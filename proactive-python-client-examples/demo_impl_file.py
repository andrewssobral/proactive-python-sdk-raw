"""
This script illustrates a basic usage scenario of the ProActive Scheduler for executing a Python task.
The steps covered in the script are as follows:

1. Connection establishment with the ProActive Scheduler using a utility function from 'utils.helper'.
2. Creation of a new job named "SimpleJob".
3. Setup of a Python task, "SimplePythonTask1", which involves specifying the task name and implementing the task logic from a file named 'random_number.py'. This demonstrates the ability to execute external Python scripts as tasks within the job.
4. Configuration of the task to use Python 3 for execution, highlighting the support for specifying the Python environment.
5. Addition of the Python task to the job, preparing it for submission.
6. Submission of the job to the ProActive Scheduler, which orchestrates the task execution based on the provided configurations.
7. Upon completion, the script ensures proper disconnection and termination of the gateway connection to the ProActive Scheduler.

This script serves as a straightforward example of how to integrate Python scripts into ProActive Scheduler jobs, showcasing the scheduler's flexibility and ease of use for managing and executing distributed tasks.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_impl_file_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask("demo_impl_file_task")
    proactive_task_1.setTaskImplementationFromFile('demo_impl_file/random_number.py')
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

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
