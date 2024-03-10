"""
House Price Prediction Using TPOT Regressor

This script demonstrates the setup and execution of a ProActive scheduler job for predicting house prices using the TPOT Regressor. TPOT (Tree-based Pipeline Optimization Tool) is an automated machine learning tool that optimizes machine learning pipelines using genetic programming. The workflow includes several key stages: loading the dataset, splitting the data, model training, and making predictions, each encapsulated within distinct ProActive tasks. These tasks are designed to execute sequentially, ensuring a comprehensive and efficient prediction pipeline.

Workflow Details:
- Load_Boston_Dataset: Loads the Boston housing dataset, a standard dataset that includes various features of houses and their corresponding prices, to serve as the basis for the prediction model.
- Split_Data: Splits the dataset into training and testing subsets, a crucial step for validating the model's predictive performance on unseen data.
- TPOT_Regressor: Initiates the TPOT Regressor to automatically search for the best machine learning pipeline for the regression problem at hand.
- Train_Model: Trains the model identified by the TPOT Regressor using the training data, fine-tuning it for optimal performance in predicting house prices.
- Download_Model: Enables the download of the trained model, allowing it to be used for predictions outside of the ProActive environment or for further analysis.
- Predict_Model: Applies the trained model to the test data to make predictions on house prices, evaluating the model's effectiveness.
- Preview_Results: Provides an initial overview of the prediction results, offering insights into the accuracy and reliability of the TPOT Regressor model in estimating house prices.

The script utilizes 'utils.helper' for seamless connectivity to the ProActive gateway, facilitating smooth job orchestration and execution. Following the job's completion, it ensures a proper disconnection and termination of the gateway, maintaining the integrity of system resources.

Please ensure the ProActive Python client and necessary dependencies are installed, and the ProActive server is accessible before running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("House_Price_Prediction_Using_TPOT_Regressor")

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

    print("Creating the TPOT_Regressor task...")
    tpot_regressor_task = bucket.create_TPOT_Regressor_task()
    proactive_job.addTask(tpot_regressor_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(tpot_regressor_task)
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
