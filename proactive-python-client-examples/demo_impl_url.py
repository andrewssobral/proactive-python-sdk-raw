"""
This script is designed for submitting a machine learning task, specifically Logistic Regression, to the ProActive Scheduler.
The script follows these steps:

1. It initiates a connection to the ProActive Scheduler gateway and retrieves the ProActive URL.
2. A job named "SimpleJob" is created.
3. A Python task named "SimplePythonTask1" is set up, with variables related to task configuration and scoring metrics.
4. The task implementation is sourced from a URL pointing to a logistic regression script in the catalog, showcasing the ability to incorporate external scripts seamlessly.
5. A fork environment is configured for the task, using a script obtained from another URL. This demonstrates the flexibility in setting up environments, which is essential for tasks requiring specific conditions or dependencies.
6. The task is then added to the job, which is subsequently submitted to the scheduler for execution.

The script emphasizes the use of external resources and environment configuration, highlighting the scheduler's capability to handle complex task setups and dependencies. It's essential to ensure the availability of the specified URLs and the scheduler's accessibility before execution.

This approach is particularly useful for machine learning workflows, where tasks may rely on specific libraries, datasets, and environments.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_impl_url_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask("demo_impl_url_task")
    proactive_task_1.addVariable("TASK_ENABLED", "True")
    proactive_task_1.addVariable("INPUT_VARIABLES", "{}")
    proactive_task_1.addVariable("SCORING", "accuracy")
    proactive_task_1.setTaskImplementationFromURL(gateway.base_url + "/catalog/buckets/ai-machine-learning/resources/Logistic_Regression_Script/raw")
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a fork environment to the proactive task #1...")
    proactive_task_1_fork_env = gateway.createForkEnvironment(language="groovy")
    proactive_task_1_fork_env.setImplementationFromURL(gateway.base_url + "/catalog/buckets/scripts/resources/fork_env_ai/raw")
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
