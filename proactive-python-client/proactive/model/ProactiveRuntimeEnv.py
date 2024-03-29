from .ProactiveForkEnv import *
from .ProactiveScriptLanguage import *

from string import Template

DEFAULT_RUNTIME_ENV_TEMPLATE = Template('''
/*
This template creates a runtime environment for containers-based jobs supporting docker, podman, and singularity.

Variables:
- CONTAINER_PLATFORM: docker, podman, singularity or null/empty (none)
- CONTAINER_IMAGE: container image name (default=activeeon/dlm3)
- CONTAINER_GPU_ENABLED: true/false, set to false to disable gpu support (default=true)
- HOST_MOUNT_PATH: optional host path to store logs
- CONTAINER_MOUNT_PATH: mounting point of optional logs in the container
- CONTAINER_ROOTLESS_ENABLED: true/false, set to false to disable rootless mode (default=false)

If used on windows:
- currently, only linux containers are supported
- make sure the drives containing the scheduler installation and TEMP folders are shared with docker containers
- the container used must have java installed by default in the /usr folder. Change the value of the java home parameter to use a different installation path

On linux, the java installation used by the ProActive Node will be also used inside the container
*/

import org.ow2.proactive.utils.OperatingSystem
import org.ow2.proactive.utils.OperatingSystemFamily
import org.codehaus.groovy.runtime.StackTraceUtils

def VERBOSE = $VERBOSE
def CONTAINER_PLATFORM = "$CONTAINER_PLATFORM"
def CONTAINER_IMAGE = "$CONTAINER_IMAGE"
def CONTAINER_GPU_ENABLED = $CONTAINER_GPU_ENABLED
def HOST_MOUNT_PATH = $HOST_MOUNT_PATH
def CONTAINER_MOUNT_PATH = $CONTAINER_MOUNT_PATH
def CONTAINER_ROOTLESS_ENABLED = $CONTAINER_ROOTLESS_ENABLED
def CONTAINER_ISOLATION_ENABLED = $CONTAINER_ISOLATION_ENABLED
def CONTAINER_NO_HOME_ENABLED = $CONTAINER_NO_HOME_ENABLED
def CONTAINER_HOST_NETWORK_ENABLED = $CONTAINER_HOST_NETWORK_ENABLED

def SUPPORTED_PLATFORMS = ["docker", "podman", "singularity"]
def CONTAINER_ENABLED = SUPPORTED_PLATFORMS.any{it.equalsIgnoreCase(CONTAINER_PLATFORM)}

def CUDA_ENABLED = false
def CUDA_HOME = System.getenv('CUDA_HOME')
def CUDA_HOME_DEFAULT = "/usr/local/cuda"
if (CUDA_HOME && (new File(CUDA_HOME)).isDirectory()) {
    CUDA_ENABLED = true
} else if ((new File(CUDA_HOME_DEFAULT)).isDirectory()) {
    CUDA_ENABLED = true
}
if (!CUDA_ENABLED) {
    CONTAINER_GPU_ENABLED = false
}

if ((new File("/.dockerenv")).exists() && ! (new File("/var/run/docker.sock")).exists()) {
    println ("Already inside docker container, without host docker access")
    CONTAINER_ENABLED = false
}

if (CONTAINER_ENABLED) {
    try {
        def sout = new StringBuffer(), serr = new StringBuffer()
        def proc = (CONTAINER_PLATFORM + ' --help').execute()
        proc.consumeProcessOutput(sout, serr)
        proc.waitForOrKill(10000)
    } catch (Exception e) {
        println CONTAINER_PLATFORM + " does not exists : " + e.getMessage()
        CONTAINER_ENABLED = false
    }
}

if (VERBOSE) {
    println "Fork environment info..."
    println "CONTAINER_ENABLED:              " + CONTAINER_ENABLED
    println "CONTAINER_PLATFORM:             " + CONTAINER_PLATFORM
    println "CONTAINER_IMAGE:                " + CONTAINER_IMAGE
    println "CONTAINER_GPU_ENABLED:          " + CONTAINER_GPU_ENABLED
    println "CUDA_ENABLED:                   " + CUDA_ENABLED
    println "HOST_MOUNT_PATH:                " + HOST_MOUNT_PATH
    println "CONTAINER_MOUNT_PATH:           " + CONTAINER_MOUNT_PATH
    println "CONTAINER_NO_HOME_ENABLED:      " + CONTAINER_NO_HOME_ENABLED
    println "CONTAINER_ROOTLESS_ENABLED:     " + CONTAINER_ROOTLESS_ENABLED
    println "CONTAINER_HOST_NETWORK_ENABLED: " + CONTAINER_HOST_NETWORK_ENABLED
}

String osName = System.getProperty("os.name")
if (VERBOSE) {
    println "Operating system : " + osName
}
OperatingSystem operatingSystem = OperatingSystem.resolveOrError(osName)
OperatingSystemFamily family = operatingSystem.getFamily()

// If docker or podman
if (CONTAINER_ENABLED && (
    "docker".equalsIgnoreCase(CONTAINER_PLATFORM) ||
    "podman".equalsIgnoreCase(CONTAINER_PLATFORM))) {

    if (CONTAINER_IMAGE.startsWith("docker://")) {
        CONTAINER_IMAGE = CONTAINER_IMAGE.substring(CONTAINER_IMAGE.indexOf("://") + 3)
    }

    // Prepare Docker parameters
    containerName = CONTAINER_IMAGE
    cmd = []
    cmd.add(CONTAINER_PLATFORM.toLowerCase())
    cmd.add("run")
    cmd.add("--rm")
    cmd.add("--shm-size=256M")

    if (CONTAINER_HOST_NETWORK_ENABLED) {
        cmd.add("--network=host")
    }

    if (CONTAINER_ROOTLESS_ENABLED) {
        cmd.add("--env")
        cmd.add("HOME=/tmp")
    }

    if (CUDA_ENABLED && CONTAINER_GPU_ENABLED) {
        if ("docker".equalsIgnoreCase(CONTAINER_PLATFORM)) {
            // Versions earlier than 19.03 require nvidia-docker2 and the --runtime=nvidia flag.
            // On versions including and after 19.03, you will use the nvidia-container-toolkit package
            // and the --gpus all flag.
            try {
                def sout = new StringBuffer(), serr = new StringBuffer()
                def proc = 'docker version -f "{{.Server.Version}}"'.execute()
                proc.consumeProcessOutput(sout, serr)
                proc.waitForOrKill(10000)
                docker_version = sout.toString()
                docker_version = docker_version.substring(1, docker_version.length()-2)
                docker_version_major = docker_version.split("\\\\.")[0].toInteger()
                docker_version_minor = docker_version.split("\\\\.")[1].toInteger()
                if (VERBOSE) {
                    println "Docker version: " + docker_version
                }
                if ((docker_version_major >= 19) && (docker_version_minor >= 3)) {
                    cmd.add("--gpus=all")
                } else {
                    cmd.add("--runtime=nvidia")
                }
            } catch (Exception e) {
                println "Error while getting the docker version: " + e.getMessage()
                println "DOCKER_GPU_ENABLED is off"
            }
        } else {
            cmd.add("--runtime=nvidia")
        }
        // rootless containers leveraging NVIDIA GPUs
        // needed when cgroups is disabled in nvidia-container-runtime
        // /etc/nvidia-container-runtime/config.toml => no-cgroups = true
        cmd.add("--privileged") // https://github.com/NVIDIA/nvidia-docker/issues/1171
    }

    isWindows = false
    isMac = false
    switch (family) {
        case OperatingSystemFamily.WINDOWS:
            isWindows = true
            break
        case OperatingSystemFamily.MAC:
            isMac = true
            break
    }
    forkEnvironment.setDockerWindowsToLinux(isWindows)

    paContainerName = System.getProperty("proactive.container.name")
    isPANodeInContainer = (paContainerName != null && !paContainerName.isEmpty())
    paContainerHostAddress = System.getProperty("proactive.container.host.address")

    if (isPANodeInContainer) {
        cmd.add("--volumes-from")
        cmd.add(paContainerName)
        cmd.add("--add-host")
        cmd.add("service-node:" + paContainerHostAddress)
    }

    // Prepare ProActive home volume
    paHomeHost = variables.get("PA_SCHEDULER_HOME")
    paHomeContainer = (isWindows ? forkEnvironment.convertToLinuxPath(paHomeHost) : paHomeHost)
    if (!isPANodeInContainer) {
        cmd.add("-v")
        cmd.add(paHomeHost + ":" + paHomeContainer)
    }
    // Prepare working directory (For Dataspaces and serialized task file)
    workspaceHost = localspace
    workspaceContainer = (isWindows ? forkEnvironment.convertToLinuxPath(workspaceHost) : workspaceHost)
    if (!isPANodeInContainer) {
        cmd.add("-v")
        cmd.add(workspaceHost + ":" + workspaceContainer)
    }

    cachespaceHost = cachespace
    cachespaceContainer = (isWindows ? forkEnvironment.convertToLinuxPath(cachespaceHost) : cachespaceHost)
    cachespaceHostFile = new File(cachespaceHost)
    if (cachespaceHostFile.exists() && cachespaceHostFile.canRead()) {
        if (!isPANodeInContainer) {
            cmd.add("-v")
            cmd.add(cachespaceHost + ":" + cachespaceContainer)
        }
    } else {
        println cachespaceHost + " does not exist or is not readable, access to cache space will be disabled in the container"
    }

    if (!isWindows && !isMac) {
        // when not on windows, mount and use the current JRE
        currentJavaHome = System.getProperty("java.home")
        forkEnvironment.setJavaHome(currentJavaHome)
        if (!isPANodeInContainer) {
            cmd.add("-v")
            cmd.add(currentJavaHome + ":" + currentJavaHome)
        }

        // when not on windows, mount a shared folder if it exists
        // sharedDirectory = new File("/shared")
        // if (sharedDirectory.isDirectory() && sharedDirectory.canWrite()) {
        //     cmd.add("-v")
        //     cmd.add("/shared:/shared")
        // }
    }

    // Prepare log directory
    if (HOST_MOUNT_PATH && CONTAINER_MOUNT_PATH) {
        cmd.add("-v")
        cmd.add(HOST_MOUNT_PATH + ":" + CONTAINER_MOUNT_PATH)
    }

    // Prepare container working directory
    cmd.add("-w")
    cmd.add(workspaceContainer)

    // linux on windows does not allow sharing identities (such as AD identities)
    if (!isWindows && CONTAINER_ROOTLESS_ENABLED) {
        sigar = new org.hyperic.sigar.Sigar()
        try {
            pid = sigar.getPid()
            creds = sigar.getProcCred(pid)
            uid = creds.getUid()
            gid = creds.getGid()
            cmd.add("--user=" + uid + ":" + gid)
        } catch (Exception e) {
            println "Cannot retrieve user or group id : " + e.getMessage()
        } finally {
            sigar.close()
        }
    }

    cmd.add(containerName)
    forkEnvironment.setPreJavaCommand(cmd)

    // Show the generated command
    if (VERBOSE) {
        println "CONTAINER COMMAND : " + forkEnvironment.getPreJavaCommand()
    }
}

// If singularity
if (CONTAINER_ENABLED &&
    "singularity".equalsIgnoreCase(CONTAINER_PLATFORM)) {

    userHome = System.getProperty("user.home")

    switch (family) {
        case OperatingSystemFamily.WINDOWS:
        throw new IllegalStateException("Singularity is not supported on Windows operating system")
        case OperatingSystemFamily.MAC:
        throw new IllegalStateException("Singularity is not supported on Mac operating system")
        default:
            isWindows = false;
    }

    if (CONTAINER_IMAGE.endsWith(".sif")) {
        sif_image_path = CONTAINER_IMAGE
    }
    else {
        try {
            imageUrl = CONTAINER_IMAGE
            imageName = imageUrl.substring(imageUrl.indexOf("://") + 3).replace("/","_").replace(":","_")
            imageLockFileName = imageName + ".lock"

            process = "singularity --version".execute()
            majorVersion = 0
            if (process.waitFor() == 0) {
                version = process.text
                version = version.replace("singularity version ", "").trim()
                if (VERBOSE) {
                    println "Singularity version: " + version
                }
                majorVersion = Integer.parseInt(version.substring(0, version.indexOf(".")))
            } else {
                throw new IllegalStateException("Cannot find singularity command")
            }

            if (majorVersion >= 3) {
                imageFile = imageName + ".sif"
            } else {
                imageFile = imageName + ".simg"
            }

            // synchronization to avoid concurrent NFS conflicts when creating the image
            imageLockPath = new File(userHome, imageLockFileName);
            if (!imageLockPath.exists()) {
                imageLockPath.createNewFile()
            } else {
                while (imageLockPath.exists()) {
                    Thread.sleep(1000)
                }
            }

            // pull the container inside the synchronization lock
            if (majorVersion >= 3) {
                pullCmd = "singularity pull --dir " + userHome + " " + imageFile + " " + imageUrl
                if (VERBOSE) {
                    println pullCmd
                }
                def env = System.getenv().collect { k, v -> "$$k=$$v" }
                env.push('XDG_RUNTIME_DIR=/run/user/$$UID')
                process = pullCmd.execute(env, new File(userHome))
            } else {
                pullCmd = "singularity pull --name " + imageFile + " " + imageUrl
                def env = System.getenv().collect { k, v -> "$$k=$$v" }
                env.push("SINGULARITY_PULLFOLDER=" + userHome)
                process = pullCmd.execute(env, new File(userHome))
            }
            
            if (VERBOSE) {
                process.in.eachLine { line ->
                    println line
                }
            }
            process.waitFor()

            (new File(userHome, imageFile)).setReadable(true, false)

            // release lock
            imageLockPath.delete()

            sif_image_path = (new File(userHome, imageFile)).getAbsolutePath()

        } catch (Exception e) {
            StackTraceUtils.deepSanitize(e)
            e.stackTrace.head().lineNumber
            throw e
        } finally {
            (new File(userHome, imageLockFileName)).delete()
        }
    }

    cmd = []
    cmd.add("singularity")
    cmd.add("exec")
    // cmd.add("--writable") // by default all singularity containers are available as read only. This option makes the file system accessible as read/write.
    cmd.add("--writable-tmpfs") // makes the file system accessible as read-write with non persistent data (with overlay support only)

    if (CONTAINER_NO_HOME_ENABLED) {
        cmd.add("--no-home") // do NOT mount users home directory if home is not the current working directory
    }

    // run a singularity image in an isolated manner
    if (CONTAINER_ISOLATION_ENABLED) {
        // cmd.add("--disable-cache") // dont use cache, and dont create cache
        // cmd.add("--cleanenv") // clean environment before running container
        // cmd.add("--contain") // use minimal /dev and empty other directories (e.g. /tmp and $$HOME) instead of sharing filesystems from your host
        cmd.add("--containall") // contain not only file systems, but also PID, IPC, and environment
    }

    if (CUDA_ENABLED && CONTAINER_GPU_ENABLED) {
        cmd.add("--nv") // enable experimental NVIDIA GPU support
    }

    // Prepare log directory
    if (HOST_MOUNT_PATH && CONTAINER_MOUNT_PATH) {
        cmd.add("-B")
        cmd.add(HOST_MOUNT_PATH + ":" + CONTAINER_MOUNT_PATH)
    }

    forkEnvironment.setDockerWindowsToLinux(isWindows)

    // Prepare ProActive home volume
    paHomeHost = variables.get("PA_SCHEDULER_HOME")
    paHomeContainer = (isWindows ? forkEnvironment.convertToLinuxPath(paHomeHost) : paHomeHost)
    cmd.add("-B")
    cmd.add(paHomeHost + ":" + paHomeContainer)
    // Prepare working directory (For Dataspaces and serialized task file)
    workspaceHost = localspace
    workspaceContainer = (isWindows ? forkEnvironment.convertToLinuxPath(workspaceHost) : workspaceHost)
    cmd.add("-B")
    cmd.add(workspaceHost + ":" + workspaceContainer)

    cachespaceHost = cachespace
    cachespaceContainer = (isWindows ? forkEnvironment.convertToLinuxPath(cachespaceHost) : cachespaceHost)
    cachespaceHostFile = new File(cachespaceHost)
    if (cachespaceHostFile.exists() && cachespaceHostFile.canRead()) {
        cmd.add("-B")
        cmd.add(cachespaceHost + ":" + cachespaceContainer)
    } else {
        println cachespaceHost + " does not exist or is not readable, access to cache space will be disabled in the container"
    }

    if (!isWindows) {
        // when not on windows, mount and use the current JRE
        currentJavaHome = System.getProperty("java.home")
        forkEnvironment.setJavaHome(currentJavaHome)
        cmd.add("-B")
        cmd.add(currentJavaHome + ":" + currentJavaHome)
    }

    // Prepare container working directory
    cmd.add("--pwd") // initial working directory for payload process inside the container
    cmd.add(workspaceContainer)
    cmd.add("--workdir") // working directory to be used for /tmp, /var/tmp and $$HOME (if -c/--contain was also used)
    cmd.add(workspaceContainer)

    // Directory containing the singularity image
    cmd.add(sif_image_path)

    forkEnvironment.setPreJavaCommand(cmd)
    forkEnvironment.addSystemEnvironmentVariable("XDG_RUNTIME_DIR",'/run/user/$$UID')

    // Show the generated command
    if (VERBOSE) {
        println "SINGULARITY COMMAND : " + forkEnvironment.getPreJavaCommand()
    }
}

if (!CONTAINER_ENABLED) {
    if (VERBOSE) {
        println "Fork environment disabled"
    }
}
''')

class ProactiveRuntimeEnv():
    """
    Represents a generic proactive runtime env script
    """

    def __create_fork_environment__(self, language="groovy"):
        return ProactiveForkEnv(language) if ProactiveScriptLanguage().is_language_supported(language) else None

    def __build_runtime_environment__(self, input_data):
        DEFAULT_CONTAINER_PLATFORM = "docker"
        DEFAULT_CONTAINER_IMAGE = "docker://activeeon/dlm3"
        DEFAULT_CONTAINER_GPU_ENABLED = "false"
        DEFAULT_HOST_MOUNT_PATH = "null"
        DEFAULT_CONTAINER_MOUNT_PATH = "null"
        DEFAULT_CONTAINER_ROOTLESS_ENABLED = "false"
        DEFAULT_CONTAINER_ISOLATION_ENABLED = "false"
        DEFAULT_CONTAINER_NO_HOME_ENABLED = "false"
        DEFAULT_CONTAINER_HOST_NETWORK_ENABLED = "true"

        CONTAINER_PLATFORM = input_data['type'] if 'type' in input_data else DEFAULT_CONTAINER_PLATFORM
        CONTAINER_IMAGE = input_data['image'] if 'image' in input_data else DEFAULT_CONTAINER_IMAGE
        CONTAINER_GPU_ENABLED = input_data['nvidia_gpu'] if 'nvidia_gpu' in input_data else DEFAULT_CONTAINER_GPU_ENABLED
        HOST_MOUNT_PATH = '"'+input_data['mount_host_path']+'"' if 'mount_host_path' in input_data else DEFAULT_HOST_MOUNT_PATH
        CONTAINER_MOUNT_PATH = '"'+input_data['mount_container_path']+'"' if 'mount_container_path' in input_data else DEFAULT_CONTAINER_MOUNT_PATH
        CONTAINER_ROOTLESS_ENABLED = input_data['rootless'] if 'rootless' in input_data else DEFAULT_CONTAINER_ROOTLESS_ENABLED
        CONTAINER_ISOLATION_ENABLED = input_data['isolation'] if 'isolation' in input_data else DEFAULT_CONTAINER_ISOLATION_ENABLED
        CONTAINER_NO_HOME_ENABLED = input_data['no_home'] if 'no_home' in input_data else DEFAULT_CONTAINER_NO_HOME_ENABLED
        CONTAINER_HOST_NETWORK_ENABLED = input_data['host_network'] if 'host_network' in input_data else DEFAULT_CONTAINER_HOST_NETWORK_ENABLED

        VERBOSE = "false"
        if 'verbose' in input_data and str.lower(input_data['verbose']) == "true":
            VERBOSE = "true"

        params = {
            'CONTAINER_PLATFORM': CONTAINER_PLATFORM,
            'CONTAINER_IMAGE': CONTAINER_IMAGE,
            'CONTAINER_GPU_ENABLED': CONTAINER_GPU_ENABLED,
            'HOST_MOUNT_PATH': HOST_MOUNT_PATH,
            'CONTAINER_MOUNT_PATH': CONTAINER_MOUNT_PATH,
            'CONTAINER_ROOTLESS_ENABLED': CONTAINER_ROOTLESS_ENABLED,
            'CONTAINER_ISOLATION_ENABLED': CONTAINER_ISOLATION_ENABLED,
            'CONTAINER_NO_HOME_ENABLED': CONTAINER_NO_HOME_ENABLED,
            'CONTAINER_HOST_NETWORK_ENABLED': CONTAINER_HOST_NETWORK_ENABLED,
            'VERBOSE': VERBOSE
        }

        template = DEFAULT_RUNTIME_ENV_TEMPLATE
        runtime_code = str(template.substitute(**params))

        return runtime_code
    
    def __create_runtime_environment__(self, input_data):
        proactive_runtime_env = self.__build_runtime_environment__(input_data)
        proactive_fork_env = self.__create_fork_environment__()
        proactive_fork_env.setImplementation(proactive_runtime_env)
        return proactive_fork_env

    def create(self, type=None, image=None, nvidia_gpu=None, mount_host_path=None, mount_container_path=None, rootless=None, isolation=None, no_home=None, host_network=None, verbose=None):
        input_data = dict()
        if type is not None:
            input_data['type'] = type
        if image is not None:
            input_data['image'] = image
        if nvidia_gpu is not None:
            input_data['nvidia_gpu'] = nvidia_gpu
        if mount_host_path is not None:
            input_data['mount_host_path'] = mount_host_path
        if mount_container_path is not None:
            input_data['mount_container_path'] = mount_container_path
        if rootless is not None:
            input_data['rootless'] = rootless
        if isolation is not None:
            input_data['isolation'] = isolation
        if no_home is not None:
            input_data['no_home'] = no_home
        if host_network is not None:
            input_data['host_network'] = host_network
        if verbose is not None:
            input_data['verbose'] = verbose
        return self.__create_runtime_environment__(input_data)
