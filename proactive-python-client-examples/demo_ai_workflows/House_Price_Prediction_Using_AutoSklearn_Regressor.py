"""
House Price Prediction Using Auto-sklearn Regressor

This script demonstrates the setup and submission of a job to the ProActive scheduler for predicting house prices using the Auto-sklearn Regressor. The workflow comprises various stages, including dataset loading, data splitting, model training, and prediction, each encapsulated within its ProActive task. These tasks are sequentially executed to construct an end-to-end prediction workflow.

Workflow Steps:
- Load_Boston_Dataset: Loads the Boston housing dataset, a classic dataset containing information about various housing features and their corresponding prices.
- Split_Data: Splits the dataset into training and testing subsets to facilitate a fair evaluation of the model's performance.
- AutoSklearn_Regressor: Initializes the Auto-sklearn Regressor, an automated machine learning tool that optimizes regression models using an ensemble of algorithms and preprocessing techniques.
- Train_Model: Trains the Auto-sklearn Regressor with the training data, allowing it to find the most effective model for predicting house prices.
- Download_Model: Makes the trained model available for download, enabling its use offline or for further analysis.
- Predict_Model: Applies the trained model to the test data to predict house prices, assessing the model's accuracy and predictive power.
- Preview_Results: Offers a sneak peek at the prediction results, giving insights into the effectiveness of the model in estimating house prices.

The script utilizes 'utils.helper' for a seamless connection to the ProActive gateway, ensuring smooth job orchestration and execution. Post-execution, it ensures a clean disconnection and termination of the gateway, preserving the integrity of system resources.

Note: Before executing the script, make sure the ProActive Python client and necessary dependencies are installed, and the ProActive server is accessible.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("House_Price_Prediction_Using_AutoSklearn_Regressor")

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

    print("Creating the AutoSklearn_Regressor task...")
    autoSklearn_regressor_task = bucket.create_Autosklearn_Regressor_task()
    proactive_job.addTask(autoSklearn_regressor_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(autoSklearn_regressor_task)
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
