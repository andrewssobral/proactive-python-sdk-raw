"""
Iris Flowers Classification Using AdaBoost

This script is designed to establish and submit a job through the ProActive scheduler for classifying iris flowers using the AdaBoost algorithm. The workflow is divided into several key steps: loading the dataset, splitting the data, training the model, and making predictions, each represented as a distinct ProActive task. These tasks are systematically arranged to be executed in order, ensuring a cohesive process for classifying iris flower species.

Workflow Overview:
- Load_Iris_Dataset: Imports the Iris dataset, a well-known dataset in machine learning that includes features of iris flowers and their species classifications.
- Split_Data: Splits the dataset into training and testing subsets, crucial for validating the model's classification accuracy.
- AdaBoost: Initializes the AdaBoost classifier, a machine learning algorithm that combines multiple weak classifiers to form a strong classifier, enhancing the model's ability to classify iris species accurately.
- Train_Model: Trains the AdaBoost classifier using the training data, fine-tuning it to identify and distinguish between different iris species.
- Download_Model: Provides the functionality to download the trained model, facilitating its use outside the ProActive environment or for further evaluations.
- Predict_Model: Applies the trained model to the test data to classify iris species, evaluating the model's classification performance.
- Preview_Results: Presents an initial look at the classification results, offering insights into the AdaBoost model's effectiveness in accurately identifying iris species.

The script employs 'utils.helper' for smooth ProActive gateway connectivity, ensuring seamless job orchestration and execution. Following the job's completion, it ensures proper gateway disconnection and termination, maintaining system and resource integrity.

Prerequisites: Ensure the ProActive Python client and the necessary dependencies are installed, and access to the ProActive server is available before running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_AdaBoost")

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

    print("Creating the AdaBoost task...")
    adaBoost_task = bucket.create_Adaboost_task()
    proactive_job.addTask(adaBoost_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(adaBoost_task)
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
