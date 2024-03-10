"""
Diabetics Detection Using TPOT Classifier

This script demonstrates setting up and submitting a job through the ProActive scheduler for detecting diabetes using the TPOT (Tree-based Pipeline Optimization Tool) Classifier. The workflow encompasses a series of steps: data importation, dataset division, model training, and prediction, with each step represented as a separate ProActive task. These tasks are arranged to execute in a specific sequence, facilitating a comprehensive workflow for diabetes detection.

Workflow Overview:
- Import_Data: Introduces the dataset into the analysis environment.
- Split_Data: Segregates the dataset into training and test subsets, essential for evaluating the model's predictive accuracy.
- TPOT_Classifier: Initializes the TPOT Classifier, an automated machine learning tool that optimizes machine learning pipelines using genetic programming.
- Train_Model: Engages the TPOT Classifier with the training subset, allowing it to identify the most effective pipeline for diabetes prediction.
- Download_Model: Enables the download of the optimized model pipeline, permitting offline utilization or subsequent analysis.
- Predict_Model: Employs the optimized pipeline to make predictions on the test subset, determining the model's effectiveness in identifying diabetic indicators.
- Preview_Results: Presents a preliminary view of the predictive outcomes, providing insights into the model's capability in diagnosing diabetes.

The script leverages 'utils.helper' for smooth connection to the ProActive gateway, ensuring efficient job orchestration and execution. After the job completes, it guarantees a proper gateway disconnection and termination, preserving system and resource integrity.

Prerequisite: Installation of the ProActive Python client and necessary dependencies, and access to the ProActive server is required before running the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Diabetics_Detection_Using_TPOT_Classifier")

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

    print("Creating the TPOT_Classifier task...")
    tpot_classifier_task = bucket.create_TPOT_Classifier_task()
    proactive_job.addTask(tpot_classifier_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(tpot_classifier_task)
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
