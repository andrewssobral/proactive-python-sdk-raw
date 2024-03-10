"""
This script demonstrates the process of creating and submitting a job to the ProActive Scheduler.
It involves the following steps:

1. Establishing a connection to the ProActive Scheduler gateway.
2. Creating a job with the name "SimpleJob".
3. Creating a Python task named "SimplePythonTask1", which prints a greeting message.
4. Adding a selection script to ensure the task runs only on Linux machines.
5. Submitting the created job to the ProActive Scheduler for execution.
6. Finally, disconnecting and terminating the gateway session.

The script makes use of utility functions from 'utils.helper' module for gateway connection and task/job management.

Please ensure the ProActive Scheduler is running and accessible, and the required scripts are present in the specified locations before executing this script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_selectionscript_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask("demo_selectionscript_task")
    proactive_task_1.setTaskImplementation("""print("Hello from " + variables.get("PA_TASK_NAME"))""")
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a selection script to the proactive task #1...")
    proactive_task_1_selection_script = gateway.createSelectionScript(language="groovy")
    proactive_task_1_selection_script.setImplementationFromFile("scripts/is_linux.groovy")  # assert proactive_task_1 only runs on linux machines
    proactive_task_1.setSelectionScript(proactive_task_1_selection_script)

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
