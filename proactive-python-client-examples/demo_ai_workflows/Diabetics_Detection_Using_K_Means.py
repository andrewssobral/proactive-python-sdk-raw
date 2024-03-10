"""
Diabetics Detection Using K-Means

This script demonstrates the construction and submission of a job to the ProActive scheduler, aimed at detecting diabetics using the K-Means clustering algorithm. The workflow includes multiple steps: data importation, data division, model training, and prediction, each encapsulated within a distinct ProActive task, executing in a specified sequence to fulfill the intended workflow.

Key Steps:
- Import_Data: Brings the dataset into the analysis framework.
- Split_Data: Segregates the dataset into training and testing subsets for a robust model evaluation.
- K_Means: Initializes the K-Means algorithm, setting the stage for clustering-based anomaly detection within the dataset.
- Train_Model: Engages the K-Means model with the training data, tuning it for optimal performance in identifying diabetic indicators.
- Download_Model: Facilitates the retrieval of the trained model, allowing for offline usage or subsequent predictions.
- Predict_Model: Employs the trained model to forecast diabetic instances within the test data, evaluating the model's effectiveness.
- Preview_Results: Offers an initial look at the prediction outcomes, giving insights into the model's diagnostic capability.

Utilization of 'utils.helper' ensures seamless connection to the ProActive gateway, managing job orchestration and execution efficiently. Post-execution, the script guarantees a tidy disconnection and closure of the gateway, maintaining system integrity.

Prerequisites include the installation of the ProActive Python client and relevant dependencies, alongside accessible ProActive server configurations.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Diabetics_Detection_Using_K_Means")

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

    print("Creating the K_Means task...")
    k_means_task = bucket.create_K_Means_task()
    proactive_job.addTask(k_means_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(k_means_task)
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
