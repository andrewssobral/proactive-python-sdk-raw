"""
This script demonstrates automating the submission of a CIFAR-10 Logistic Regression training pipeline as a job to the ProActive scheduler. The job is designed to run in a Docker container, ensuring a consistent environment for the training task. The process involves setting up the job and task, configuring the Docker environment, handling input and output files, and executing a pre-script for environment preparation.

Key Features:
- Creation of a ProActive job named 'CIFAR-10_Logistic_Regression_Pipeline'.
- Configuration of a Python task to execute the 'train.py' script for model training.
- Use of a Docker runtime environment to ensure task consistency across executions.
- Inclusion of 'requirements.txt' and the entire 'dataset' directory as input files to the task.
- Specification of the 'models' directory for output file storage.
- Implementation of a bash pre-script to update the container, install dependencies, and download the CIFAR-10 dataset.

Usage:
- The script requires access to a ProActive scheduler and the 'utils.helper' module for ProActive gateway connectivity.
- Ensure Docker is available and configured correctly in the ProActive scheduler nodes.
- The 'dataset/download_dataset.sh' script must be present and executable for dataset preparation.

This script exemplifies the integration of ProActive's scheduling capabilities with Docker for machine learning workflows, illustrating an efficient approach to managing and automating data science tasks.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    # Start setting up a new job
    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("CIFAR-10_Logistic_Regression_Pipeline")

    # Create and configure the first task of the job
    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask('Train')
    proactive_task_1.setTaskImplementationFromFile("train.py")
    # Set the runtime environment for the task using Docker
    proactive_task_1.setRuntimeEnvironment(
        type="docker", image="python:3.9-slim",
        mount_host_path="/shared", mount_container_path="/shared"
    )
    # Specify input file(s)/folder(s) required by the task
    proactive_task_1.addInputFile('requirements.txt')
    proactive_task_1.addInputFile('dataset/**')
    # Specify output file(s)/folder(s) generated by the task
    proactive_task_1.addOutputFile('models/logistic_regression_model.pkl')

    # Add a pre-script to prepare the environment before the task runs
    print("Adding a pre-script to task #1...")
    pre_script = gateway.createPreScript(language='bash')
    pre_script.setImplementation("""
        apt-get -qq update && apt-get install -y wget unzip
        pip install -r requirements.txt
        chmod +x ./dataset/download_dataset.sh
        cd dataset && ./download_dataset.sh
    """)
    proactive_task_1.setPreScript(pre_script)

    # Add the configured task to the job
    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

    # Submit the job to the ProActive scheduler and print the job ID
    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJobWithInputsAndOutputsPaths(proactive_job)
    print("job_id: " + str(job_id))

    print("Getting job output...")
    job_output = gateway.getJobOutput(job_id)
    print(job_output)

finally:
    # Ensure the gateway disconnects even if an error occurs
    print("Disconnecting")
    gateway.disconnect()
    print("Disconnected")
    # Terminate the gateway instance
    gateway.terminate()
    print("Finished")