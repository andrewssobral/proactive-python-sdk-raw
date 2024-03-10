"""
Iris Flowers Classification Using Gaussian Naive Bayes

This script demonstrates configuring and submitting a job through the ProActive scheduler for classifying Iris flower species using the Gaussian Naive Bayes algorithm. The workflow is structured into several phases: loading the dataset, splitting the data, training the model, and making predictions, with each phase represented as an individual ProActive task. These tasks are designed to be executed in a specific order to ensure a smooth and efficient classification process.

Workflow Overview:
- Load_Iris_Dataset: Imports the Iris dataset, which contains various features of Iris flowers and their corresponding classifications, forming the foundation for this classification task.
- Split_Data: Segments the dataset into training and testing subsets, crucial for accurately evaluating the model's performance in classification.
- Gaussian_Naive_Bayes: Implements the Gaussian Naive Bayes classifier, a simple yet effective probabilistic classifier based on applying Bayes' theorem with the assumption of independence among predictors.
- Train_Model: Trains the Gaussian Naive Bayes model using the training subset, calibrating it to classify Iris species based on the input features.
- Download_Model: Allows the trained model to be downloaded, enabling its application in various contexts or for further examination.
- Predict_Model: Uses the trained model to classify Iris flowers in the test subset, determining the model's accuracy and reliability in species identification.
- Preview_Results: Provides an initial look at the classification results, shedding light on the Gaussian Naive Bayes classifier's capability in correctly identifying Iris flower species.

The script utilizes 'utils.helper' for straightforward connectivity to the ProActive gateway, facilitating effective job orchestration and execution. After the job concludes, it ensures proper disconnection and termination of the gateway, preserving the integrity of system resources.

Prerequisites: Ensure the ProActive Python client and necessary dependencies are installed, and the ProActive server is accessible before executing the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_Gaussian_Naive_Bayes")

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

    print("Creating the Gaussian_Naive_Bayes task...")
    gaussian_bayes_task = bucket.create_Gaussian_Naive_Bayes_task()
    proactive_job.addTask(gaussian_bayes_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(gaussian_bayes_task)
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
