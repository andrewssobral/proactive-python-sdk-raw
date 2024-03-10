"""
Iris Flowers Classification Using Support Vector Machines

This script details the configuration and submission of a ProActive scheduler job intended for the classification of Iris flower species through Support Vector Machines (SVM). The workflow is segmented into various stages, encompassing dataset acquisition, data division, model training, and subsequent prediction, each represented as an individual ProActive task. These tasks are arranged to execute in a predetermined sequence, facilitating a cohesive and effective classification mechanism.

Workflow Breakdown:
- Load_Iris_Dataset: Retrieves the Iris dataset, comprising assorted features of Iris flowers alongside their classifications, establishing the groundwork for the classification task.
- Split_Data: Segregates the dataset into training and testing subsets, crucial for an unbiased appraisal of the model's classification efficacy.
- Support_Vector_Machines: Implements the SVM classifier, a powerful machine learning model known for its capability in handling high-dimensional spaces and effectiveness in classification scenarios.
- Train_Model: Trains the SVM model using the training data, adjusting it to proficiently classify Iris species based on their characteristics.
- Download_Model: Enables the download of the trained model, permitting its utilization in different scenarios or for further scrutiny.
- Predict_Model: Employs the trained model to classify Iris flowers within the testing subset, assessing the model's precision and classification performance.
- Preview_Results: Provides an initial overview of the classification results, elucidating the SVM classifier's accuracy in distinguishing Iris flower species.

Leveraging 'utils.helper' for streamlined connectivity to the ProActive gateway, the script ensures efficient job orchestration and execution. Post-execution, it manages a proper disconnection and shutdown of the gateway, safeguarding the integrity of system resources.

Prerequisites: Ensure the installation of the ProActive Python client and necessary dependencies, and confirm the ProActive server's accessibility prior to executing the script.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_Support_Vector_Machines")

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

    print("Creating the Support_Vector_Machines task...")
    support_vector_machines_task = bucket.create_Support_Vector_Machines_task()
    proactive_job.addTask(support_vector_machines_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(support_vector_machines_task)
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
