"""
This script demonstrates setting up and executing a machine learning workflow for the Iris dataset using the ProActive Scheduler. The workflow consists of several tasks, each representing a step in the machine learning pipeline, including data loading, preprocessing, model training, prediction, and result visualization.

Steps:
1. Establishes a connection to the ProActive Scheduler and creates a new job named "ai_machine_learning_workflow".
2. Retrieves a predefined bucket "ai-machine-learning" containing task templates for machine learning operations.
3. Sequentially creates and configures tasks for loading the Iris dataset, splitting data, logistic regression model preparation, model training, model downloading, making predictions with the trained model, and previewing results.
4. Each task is added to the job, with dependencies set up to ensure the correct execution order.
5. The job is submitted to the ProActive Scheduler for execution, and the script awaits and prints the job's output upon completion.

This script emphasizes the use of the ProActive Scheduler for orchestrating complex workflows, particularly in the context of machine learning, showcasing its capability to manage dependencies and execute tasks in an ordered and efficient manner.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("demo_ai_workflow")

    print("Getting the ai-machine-learning bucket")
    bucket = gateway.getBucket("ai-machine-learning")

    # ------------------------------------------------------------------------

    print("Creating the Load_Iris_Dataset task...")
    load_iris_dataset_task = bucket.create_Load_Iris_Dataset_task()
    proactive_job.addTask(load_iris_dataset_task)

    print("Creating the Split_Data task...")
    split_data_task = bucket.create_Split_Data_task()
    split_data_task.addDependency(load_iris_dataset_task)
    proactive_job.addTask(split_data_task)

    print("Creating the Logistic_Regression task...")
    logistic_regression_task = bucket.create_Logistic_Regression_task()
    proactive_job.addTask(logistic_regression_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(logistic_regression_task)
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
