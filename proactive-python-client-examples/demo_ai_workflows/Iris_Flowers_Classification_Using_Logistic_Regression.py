"""
Iris Flowers Classification Using Logistic Regression

This script outlines the procedure for setting up and executing a job via the ProActive scheduler to classify Iris flower species using Logistic Regression. The process encompasses several key steps: dataset acquisition, data segmentation, model training, and prediction, each encapsulated within a distinct ProActive task. These tasks are arranged to run in sequence, ensuring a seamless and logical flow for the classification endeavor.

Workflow Synopsis:
- Load_Iris_Dataset: Retrieves the Iris dataset, encompassing a variety of Iris flower features and their corresponding species classifications, forming the basis of the classification task.
- Split_Data: Segments the dataset into training and testing subsets, pivotal for an objective evaluation of the model's classification accuracy.
- Logistic_Regression: Deploys the Logistic Regression model, a fundamental machine learning algorithm for binary and multiclass classification tasks, renowned for its simplicity and efficiency.
- Train_Model: Trains the Logistic Regression model with the training subset, tuning it to discern between different Iris flower species based on their characteristics.
- Download_Model: Facilitates the downloading of the trained model, making it available for application in diverse settings or for additional scrutiny.
- Predict_Model: Employs the trained model to classify Iris flowers in the testing subset, gauging the model's precision and effectiveness in species identification.
- Preview_Results: Presents a preliminary examination of the classification results, providing insights into the Logistic Regression model's proficiency in accurately classifying Iris flower species.

The script employs 'utils.helper' for straightforward ProActive gateway connectivity, guaranteeing efficient job orchestration and execution. Following the job's conclusion, it ensures a proper disconnection and cessation of the gateway, safeguarding the integrity of system and resource allocations.

Prerequisites: Verify the installation of the ProActive Python client and necessary dependencies, and ensure accessibility to the ProActive server before running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_Logistic_Regression")

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
