"""
House Price Prediction Using Bayesian Ridge Regression

This script sets up and submits a job to the ProActive scheduler to predict house prices utilizing Bayesian Ridge Regression. The process is structured into several phases, including data loading, data partitioning, model training, and prediction. Each of these phases is represented as a discrete ProActive task, designed to be executed in sequence, thus forming a comprehensive predictive analysis workflow.

Workflow Description:
- Load_Boston_Dataset: Initiates the process by loading the Boston housing dataset, which comprises various features of houses and their corresponding prices, serving as the foundation for the predictive analysis.
- Split_Data: Segregates the loaded dataset into training and testing sets, a crucial step for unbiased model evaluation.
- Bayesian_Ridge_Regression: Introduces the Bayesian Ridge Regression task, a regression technique that incorporates Bayesian inference to provide a probabilistic approach to linear regression, offering insights into uncertainty and variance in the predictions.
- Train_Model: Trains the Bayesian Ridge Regression model using the training subset, optimizing it for accurate and reliable house price prediction.
- Download_Model: Enables the downloading of the trained model, allowing for its application in offline scenarios or further evaluative studies.
- Predict_Model: Employs the trained model to forecast house prices on the testing subset, gauging the model's predictive accuracy and reliability.
- Preview_Results: Presents an initial review of the predictive outcomes, shedding light on the model's capability in estimating house prices accurately.

Utilizing 'utils.helper', the script ensures a seamless connection to the ProActive gateway, facilitating efficient job orchestration and execution. Following the job's completion, it secures a proper disconnection and termination of the gateway, safeguarding the integrity and efficiency of system resources.

Prerequisites: Ensure the installation of the ProActive Python client, along with the necessary dependencies, and verify the accessibility of the ProActive server prior to executing the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("House_Price_Prediction_Using_Bayesian_Ridge_Regression")

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

    print("Creating the Bayesian_Ridge_Regression task...")
    bayesian_ridge_regression_task = bucket.create_Bayesian_Ridge_Regression_task()
    proactive_job.addTask(bayesian_ridge_regression_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(bayesian_ridge_regression_task)
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
