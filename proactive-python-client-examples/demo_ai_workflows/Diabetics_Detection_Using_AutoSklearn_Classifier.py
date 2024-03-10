"""
Diabetics Detection Using AutoSklearn Classifier

This script leverages the ProActive Workflows & Scheduling platform to create and manage a machine learning job aimed at detecting diabetes. It utilizes the AutoSklearn Classifier within a sequence of tasks that include data importation, preprocessing, model training, prediction, and result visualization. The process is orchestrated through a series of dependent tasks, each handling a specific part of the workflow within the 'ai-machine-learning' bucket.

The script performs the following steps:
1. Establishes a connection with the ProActive Gateway.
2. Creates a new ProActive job with a descriptive name.
3. Adds tasks for data importation, splitting, classification, model training, model downloading, prediction, and result preview.
4. Submits the job to the ProActive scheduler and fetches the job output upon completion.

Usage:
- Ensure the ProActive Python client is properly installed and configured.
- Run the script in an environment where the ProActive Python client is accessible.

Notes:
- The script assumes the existence of predefined tasks within the 'ai-machine-learning' bucket on the ProActive server.
- Proper error handling is implemented to ensure graceful disconnection and termination of the gateway connection.

Dependencies:
- utils.helper.getProActiveGateway: A utility function to establish a connection with the ProActive Gateway.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Diabetics_Detection_Using_AutoSklearn_Classifier")

    print("Getting the ai-machine-learning bucket")
    bucket = gateway.getBucket("ai-machine-learning")

    # ------------------------------------------------------------------------

    print("Creating the Import_Data task...")
    import_data_dataset_task = bucket.create_Import_Data_task()
    proactive_job.addTask(import_data_dataset_task)

    print("Creating the Split_Data task...")
    split_data_task = bucket.create_Split_Data_task()
    split_data_task.addDependency(import_data_dataset_task)
    proactive_job.addTask(split_data_task)

    print("Creating the AutoSklearn_Classifier task...")
    autoSklearn_classifier_task = bucket.create_Autosklearn_Classifier_task()
    proactive_job.addTask(autoSklearn_classifier_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(autoSklearn_classifier_task)
    proactive_job.addTask(train_model_task)

    print("Creating the Download_Model task...")
    download_model_task = bucket.create_Download_Model_task()
    download_model_task.addDependency(train_model_task)
    proactive_job.addTask(download_model_task)

    print("Creating the Predict_Model task...")
    predict_model_task = bucket.create_Predict_Model_task()
    predict_model_task.addDependency(split_data_task)
    predict_model_task.addDependency(train_model_task)
    proactive_job.addTask(predict_model_task)

    print("Creating the Preview_Results task...")
    preview_results_task = bucket.create_Preview_Results_task()
    preview_results_task.addDependency(predict_model_task)
    proactive_job.addTask(preview_results_task)

    # ------------------------------------------------------------------------

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
