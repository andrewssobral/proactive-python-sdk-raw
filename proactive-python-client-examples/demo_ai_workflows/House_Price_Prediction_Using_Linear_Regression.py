"""
House Price Prediction Using Linear Regression

This script outlines the process for setting up and submitting a ProActive scheduler job aimed at predicting house prices using Linear Regression. The workflow incorporates several stages: dataset loading, data partitioning, model training, and prediction, each encapsulated within a distinct ProActive task. These tasks are methodically arranged to execute in sequence, enabling a structured approach to house price prediction.

Workflow Summary:
- Load_Boston_Dataset: Fetches the Boston housing dataset, which is a renowned dataset containing features of houses and their respective prices, serving as the basis for prediction.
- Split_Data: Divides the dataset into training and testing subsets, which is crucial for an unbiased assessment of the model's prediction capabilities.
- Linear_Regression: Initializes the Linear Regression model, a fundamental approach to understanding relationships between variables and predicting outcomes.
- Train_Model: Trains the Linear Regression model with the training subset, optimizing it to predict house prices based on the dataset's features.
- Download_Model: Allows for the retrieval of the trained model, enabling its application outside the ProActive environment or for further evaluations.
- Predict_Model: Utilizes the trained model to estimate house prices on the test subset, gauging the model's predictive accuracy and reliability.
- Preview_Results: Provides an initial look at the prediction outcomes, offering insights into the Linear Regression model's effectiveness in house price estimation.

The script employs 'utils.helper' for seamless connectivity to the ProActive gateway, ensuring efficient orchestration and execution of the job. Following the completion of the job, the script ensures a clean disconnection and termination of the gateway, safeguarding system and resource integrity.

Please ensure the ProActive Python client and necessary dependencies are installed, and the ProActive server is accessible prior to running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("House_Price_Prediction_Using_Linear_Regression")

    print("Getting the ai-machine-learning bucket")
    bucket = gateway.getBucket("ai-machine-learning")

    # ------------------------------------------------------------------------

    print("Creating the Load_Boston_Dataset task...")
    load_boston_dataset_task = bucket.create_Load_Boston_Dataset_task()
    proactive_job.addTask(load_boston_dataset_task)

    print("Creating the Split_Data task...")
    split_data_task = bucket.create_Split_Data_task()
    split_data_task.addDependency(load_boston_dataset_task)
    proactive_job.addTask(split_data_task)

    print("Creating the Linear_Regression task...")
    linear_regression_task = bucket.create_Linear_Regression_task()
    proactive_job.addTask(linear_regression_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(linear_regression_task)
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
