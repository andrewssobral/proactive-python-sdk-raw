"""
Diabetics Detection Using One-Class SVM

This script sets up and submits a ProActive scheduler job for detecting diabetes using a One-Class SVM (Support Vector Machine) algorithm. The procedure comprises multiple phases: data importation, dataset splitting, model training, and predictions. Each phase is encapsulated in a distinct ProActive task, orchestrated to execute sequentially to complete the detection workflow.

Workflow Summary:
- Import_Data: Loads the dataset for analysis.
- Split_Data: Divides the dataset into training and testing subsets to evaluate the model's performance accurately.
- One_Class_SVM: Configures the One-Class SVM algorithm for anomaly detection within the dataset, particularly suited for identifying outliers or abnormal patterns.
- Train_Model: Trains the One-Class SVM model with the training data subset, fine-tuning it for optimal anomaly detection related to diabetes.
- Download_Model: Provides the functionality to download the trained model for offline use or further analysis.
- Predict_Model: Utilizes the trained model to predict diabetic conditions in the test dataset, assessing the model's predictive capabilities.
- Preview_Results: Displays an initial overview of the prediction results, offering insights into the model's effectiveness in detecting diabetic conditions.

The script employs 'utils.helper' for efficient connectivity to the ProActive gateway, managing the orchestration and execution of the job. Following the execution, it ensures a proper disconnection and termination of the gateway, maintaining the integrity of the system and resources.

Note: Ensure the ProActive Python client and relevant dependencies are installed, and the ProActive server is accessible before executing the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Diabetics_Detection_Using_One_Class_SVM")

    print("Getting the ai-machine-learning bucket")
    bucket = gateway.getBucket("ai-machine-learning")

    # ------------------------------------------------------------------------

    print("Creating the Import_Data task...")
    import_data_dataset_task = bucket.create_Import_Data_task()
    proactive_job.addTask(import_data_dataset_task)

    print("Creating the Split_Data task...")
    split_data_task = bucket.create_Split_Data_task()
    split_data_task.addDependency(import_data_dataset_task)
    proactive_job.addTask(split_data_task)

    print("Creating the One_Class_SVMtask...")
    one_class_svm_task = bucket.create_One_Class_SVM_task()
    proactive_job.addTask(one_class_svm_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(one_class_svm_task)
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
