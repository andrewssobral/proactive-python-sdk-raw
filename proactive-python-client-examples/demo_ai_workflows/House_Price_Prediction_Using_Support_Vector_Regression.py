"""
House Price Prediction Using Support Vector Regression

This script sets up and submits a job to the ProActive scheduler for predicting house prices utilizing Support Vector Regression (SVR). The workflow is composed of multiple phases, including dataset loading, data partitioning, model training, and prediction, with each phase represented as an individual ProActive task. These tasks are organized to execute in a defined sequence, facilitating a streamlined prediction process.

Workflow Description:
- Load_Boston_Dataset: Retrieves the Boston housing dataset, a well-known dataset featuring various housing characteristics and their prices, which serves as the foundation for prediction.
- Split_Data: Segregates the dataset into training and testing subsets, essential for a fair evaluation of the model's predictive performance.
- Support_Vector_Regression: Deploys the Support Vector Regression model, an advanced regression technique known for its effectiveness in capturing complex relationships within data.
- Train_Model: Trains the SVR model using the training subset, calibrating it to accurately predict house prices based on the available features.
- Download_Model: Enables the downloading of the trained model, allowing for its application in different contexts or for further analysis.
- Predict_Model: Applies the trained model to the test subset to forecast house prices, assessing the model's accuracy and efficacy in prediction.
- Preview_Results: Offers a preliminary view of the prediction results, providing insight into the SVR model's capability in estimating house prices accurately.

The script leverages 'utils.helper' for efficient ProActive gateway connectivity, ensuring seamless job orchestration and execution. Upon job completion, it ensures proper gateway disconnection and termination, maintaining the integrity of system resources.

Note: Installation of the ProActive Python client and the required dependencies, along with access to the ProActive server, should be confirmed before executing the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("House_Price_Prediction_Using_Support_Vector_Regression")

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

    print("Creating the Support_Vector_Regression task...")
    support_vector_regression_task = bucket.create_Support_Vector_Regression_task()
    proactive_job.addTask(support_vector_regression_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(support_vector_regression_task)
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
