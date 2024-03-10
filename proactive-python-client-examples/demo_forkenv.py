"""
This script showcases the creation and execution of a Python task within a ProActive Scheduler job, emphasizing task customization and execution environment configuration. The process unfolds as follows:

1. A connection is established with the ProActive Scheduler through a utility function provided by 'utils.helper'.
2. A job named "SimpleJob" is created, serving as a container for the tasks that will be executed.
3. The script then sets up a Python task named "SimplePythonTask1". This task is designed to print a greeting message and the Python version of the runtime environment. The task implementation is defined inline within the script, demonstrating the flexibility of embedding task logic directly in the script.
4. The Python task is configured to run using Python 3, ensuring compatibility with the specified task implementation.
5. A fork environment is added to the Python task, configured through a Groovy script located in "scripts/fork_env.groovy". This environment setup allows for more advanced task execution conditions, such as specifying the use of Docker as the container platform through task variables. This highlights the scheduler's capability to accommodate complex execution environments, catering to tasks with specific runtime requirements.
6. The Python task is then added to the job, making it ready for submission to the ProActive Scheduler.
7. The job is submitted to the scheduler, and the script prints the job ID as a reference. The scheduler takes over from here, managing the execution of the job according to its configuration and the scheduler's policies.
8. After submission, the script fetches and prints the output of the job, allowing for immediate feedback on the task execution.

Finally, the script ensures a clean disconnection and termination of the gateway connection to the ProActive Scheduler, emphasizing the importance of resource management and cleanup post-execution.

This script exemplifies a basic yet powerful use case of the ProActive Scheduler for executing Python tasks with specific runtime environments, demonstrating both task and environment configurability.
"""
from utils.helper import getProActiveGateway

proactive_task_1_impl = """
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version())
"""

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_forkenv_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask("demo_forkenv_task")
    proactive_task_1.setTaskImplementation(proactive_task_1_impl)
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a fork environment to the proactive task #1...")
    proactive_task_1_fork_env = gateway.createForkEnvironment(language="groovy")
    proactive_task_1_fork_env.setImplementationFromFile("scripts/fork_env.groovy")
    proactive_task_1.setForkEnvironment(proactive_task_1_fork_env)
    proactive_task_1.addVariable("CONTAINER_PLATFORM", "docker")

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJob(proactive_job, debug=False)
    print("job_id: " + str(job_id))

    print("Getting job output...")
    job_output = gateway.getJobOutput(job_id)
    print(job_output)

finally:
    print("Disconnecting")
    gateway.disconnect()
    print("Disconnected")
    gateway.terminate()
    print("Finished")
