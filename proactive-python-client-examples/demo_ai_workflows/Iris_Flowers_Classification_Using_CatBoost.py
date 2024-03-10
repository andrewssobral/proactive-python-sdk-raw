"""
Iris Flowers Classification Using CatBoost

This script is designed to demonstrate the creation and submission of a ProActive scheduler job for the classification of Iris flowers using the CatBoost algorithm. The workflow comprises several key stages, including dataset loading, data splitting, model training, and prediction, each represented by an individual ProActive task. These tasks are orchestrated to execute in a sequential manner, ensuring a coherent and effective classification process.

Workflow Breakdown:
- Load_Iris_Dataset: Loads the Iris dataset, which consists of features related to Iris flowers and their corresponding classifications, serving as the foundation for the classification task.
- Split_Data: Splits the dataset into training and testing subsets, critical for the objective assessment of the model's classification capabilities.
- Catboost: Initializes the CatBoost classifier, a high-performance machine learning algorithm known for its effectiveness in handling categorical data and achieving high accuracy levels.
- Train_Model: Trains the CatBoost classifier with the training subset, optimizing it to accurately classify Iris flower species based on the given features.
- Download_Model: Provides functionality to download the trained model, allowing for its use in different contexts or for further evaluation.
- Predict_Model: Applies the trained model to the test subset to classify Iris flowers, evaluating the model's precision and effectiveness in classification.
- Preview_Results: Offers an initial glance at the classification results, providing insights into the CatBoost classifier's ability to accurately identify Iris flower species.

The script employs 'utils.helper' for seamless connectivity to the ProActive gateway, facilitating efficient job orchestration and execution. Upon the job's completion, it ensures a proper gateway disconnection and termination, preserving the integrity of system resources.

Prerequisites: Ensure that the ProActive Python client and required dependencies are installed, and the ProActive server is accessible prior to running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_CatBoost")

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

    print("Creating the Catboost task...")
    catboost_task = bucket.create_Catboost_task()
    proactive_job.addTask(catboost_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(catboost_task)
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
