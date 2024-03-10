"""
Iris Flowers Classification Using XGBoost

This script is engineered to set up and submit a ProActive scheduler job dedicated to classifying Iris flower species utilizing the XGBoost algorithm. The process encompasses several key phases: loading the dataset, splitting the data, model training, and performing predictions, each represented as a distinct ProActive task. These tasks are systematically organized to execute in sequence, enabling a thorough and efficient approach to classification.

Workflow Sequence:
- Load_Iris_Dataset: Accesses the Iris dataset, which includes a variety of Iris flower features and their corresponding classifications, providing a foundational dataset for the classification task.
- Split_Data: Portions the dataset into training and testing subsets, essential for accurately evaluating the model's classification ability.
- XGBoost: Deploys the XGBoost classifier, an optimized distributed gradient boosting library designed to be highly efficient, flexible, and portable, known for its performance and speed in classification tasks.
- Train_Model: Engages the XGBoost model with the training subset, optimizing it for accurate classification of Iris species based on input features.
- Download_Model: Makes the trained model available for download, allowing for its application in various contexts or for additional analysis.
- Predict_Model: Applies the trained model to the test subset to classify Iris flowers, assessing the model's accuracy and classification efficacy.
- Preview_Results: Offers a preliminary insight into the classification outcomes, highlighting the XGBoost classifier's effectiveness in accurately identifying Iris flower species.

The script uses 'utils.helper' for seamless connectivity to the ProActive gateway, ensuring smooth job orchestration and execution. After the completion of the job, it ensures proper disconnection and cessation of the gateway, maintaining system and resource integrity.

Pre-requisites: Ensure the ProActive Python client and necessary dependencies are installed, and verify the ProActive server's accessibility before running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_XGBoost")

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

    print("Creating the XGBoost task...")
    xgboost_task = bucket.create_XGBoost_task()
    proactive_job.addTask(xgboost_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(xgboost_task)
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
