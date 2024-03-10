"""
This script illustrates a straightforward example of utilizing the ProActive Scheduler to execute a simple Python task. The procedural steps encapsulated in this script include:

1. Establishing a connection with the ProActive Scheduler via the 'getProActiveGateway' function provided by the 'utils.helper' module, demonstrating the ease of integrating ProActive Scheduler functionalities.
2. Initiating the creation of a new job titled "SimpleJob," which acts as a container for one or more tasks that will be managed and executed by the scheduler.
3. Defining a Python task, named "SimplePythonTask1," with an inline implementation that prints a greeting and the Python version being used. This showcases the capability to embed Python code directly within the task configuration, facilitating quick and dynamic task setups.
4. Specifying that the Python task should be executed using Python 3, as indicated by the addition of generic information. This detail ensures compatibility and consistency across different execution environments.
5. Adding the configured Python task to the previously created job, thereby assembling the job's structure and its constituent tasks.
6. Submitting the assembled job to the ProActive Scheduler for execution. The scheduler is then responsible for managing the job's lifecycle, including task scheduling, execution, and resource allocation.
7. Retrieving and printing the output of the job, allowing for immediate visibility into the execution results. This step is crucial for debugging and verifying the correctness of the task's implementation.
8. Ensuring a graceful disconnection and termination of the gateway connection to the ProActive Scheduler, highlighting the importance of proper resource management and cleanup after job submission.

This script serves as a basic demonstration of submitting and executing a Python task within the ProActive Scheduler environment, emphasizing simplicity and ease of use. It provides a foundation for more complex scheduling and task execution scenarios.
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
    proactive_job.setJobName("demo_basic_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask("demo_basic_task")
    proactive_task_1.setTaskImplementation(proactive_task_1_impl)
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJob(proactive_job)
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
