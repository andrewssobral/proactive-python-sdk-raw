"""
This script demonstrates the creation and submission of a ProActive job that includes a single Bash task designed to count the number of files within a specified directory, outputting the count both to the terminal and to a file within the same directory. The task showcases file handling in ProActive tasks, particularly how to include input files for processing and designate output files to capture task results. This example is particularly useful for understanding data transfer and file management in ProActive workflows.

Key Steps:
- Establishes a connection to the ProActive scheduler and creates a new job.
- Sets up a Bash task that counts files in the 'demo_transf_file' directory, saving the count to 'file_count.txt' within the same directory.
- Demonstrates the use of input and output files in ProActive tasks, specifying patterns to include all files within a directory for processing and result generation.
- Submits the job to the ProActive scheduler, retrieves, and prints the job output to the console.

Ensure the ProActive scheduler is accessible and the 'utils.helper' module is correctly set up before executing this script.
"""
from utils.helper import getProActiveGateway

proactive_task_1_impl = """
echo "Hello from $variables_PA_TASK_NAME"
pwd && find .

# Specify the directory to count files in
DIRECTORY="./demo_transf_file"

# Count the number of files in the specified directory (excluding directories)
FILE_COUNT=$(find "$DIRECTORY" -type f | wc -l)

# Print the file count to the terminal
echo "Number of files in $DIRECTORY: $FILE_COUNT"

# Specify the filename where the result should be saved inside the DIRECTORY
RESULT_FILE="$DIRECTORY/file_count.txt"

# Write the file count to the specified result file inside the directory
echo "Number of files in $DIRECTORY: $FILE_COUNT" > "$RESULT_FILE"
"""

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_transf_file_job")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createTask(language="bash", task_name="demo_transf_file_task")
    proactive_task_1.setTaskImplementation(proactive_task_1_impl)
    proactive_task_1.addInputFile('demo_transf_file/**')
    proactive_task_1.addOutputFile('demo_transf_file/**')

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJobWithInputsAndOutputsPaths(proactive_job)
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
