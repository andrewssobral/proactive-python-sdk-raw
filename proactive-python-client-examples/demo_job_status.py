"""
ProActive Job Submission and Monitoring Script

This script demonstrates the end-to-end process of job submission and monitoring using the ProActive Python SDK. 

It covers creating a ProActive job, adding a Python task, submitting the job to the ProActive Scheduler, and monitoring the job status until completion. 

The script concludes by retrieving and displaying the job's output.
"""
import time
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    # Create and configure a ProActive job and task
    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_job_status")

    print("Creating a proactive task...")
    proactive_task = gateway.createPythonTask("demo_job_status_task")
    proactive_task.setTaskImplementation('print("Execution completed")')

    print("Adding proactive task to the proactive job...")
    proactive_job.addTask(proactive_task)

    # Submit the job to the ProActive scheduler
    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJob(proactive_job)
    print(f"Job submitted with ID: {job_id}")

    # Monitor job status
    is_finished = False
    while not is_finished:
        # Get the current state of the job
        job_status = gateway.getJobStatus(job_id)
        
        # Print the current job status
        print(f"Current job status: {job_status}")
        
        # Check if the job has finished
        if job_status.upper() in ["FINISHED", "CANCELED", "FAILED"]:
            is_finished = True
        else:
            # Wait for a few seconds before checking again
            time.sleep(.5)

    # Retrieve and print job results
    print("Job output:")
    print(gateway.getJobOutput(job_id))

finally:
    # Cleanup
    gateway.disconnect()
    gateway.terminate()
    print("Disconnected and finished.")
