"""
Iris Flowers Classification Using Random Forest

This script is crafted to demonstrate the setup and execution of a ProActive scheduler job for classifying Iris flower species utilizing the Random Forest algorithm. The process is divided into distinct phases: dataset ingestion, data segmentation, model training, and prediction, each encapsulated in a separate ProActive task. These tasks are methodically arranged to be executed in sequence, ensuring an effective and systematic approach to classification.

Workflow Composition:
- Load_Iris_Dataset: Imports the Iris dataset, encompassing various features of Iris flowers alongside their categorizations, providing a solid base for the classification endeavor.
- Split_Data: Splits the dataset into training and testing portions, a vital step for objectively assessing the model's classification prowess.
- Random_Forest: Deploys the Random Forest classifier, a robust ensemble learning method that constructs multiple decision trees and merges their predictions, known for its high accuracy and ability to avoid overfitting.
- Train_Model: Trains the Random Forest model with the training subset, fine-tuning it for precise classification of Iris species based on the provided features.
- Download_Model: Facilitates the downloading of the trained model, enabling its application in various settings or for subsequent analysis.
- Predict_Model: Engages the trained model to classify Iris flowers within the test subset, evaluating the model's effectiveness and accuracy in species identification.
- Preview_Results: Offers a preliminary glimpse into the classification outcomes, shedding light on the Random Forest classifier's capacity to accurately discern Iris flower species.

Utilizing 'utils.helper' for streamlined ProActive gateway connectivity, the script ensures smooth job orchestration and execution. Following the job's conclusion, it manages a proper gateway disconnection and cessation, maintaining the sanctity of system and resource integrity.

Pre-requisites: Confirm the installation of the ProActive Python client and requisite dependencies, and verify accessibility to the ProActive server prior to script execution.
"""
from utils.helper import getProActiveGateway

try:
    gateway = getProActiveGateway()

    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("Iris_Flowers_Classification_Using_Random_Forest")

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

    print("Creating the Random_Forest task...")
    random_forest_task = bucket.create_Random_Forest_task()
    proactive_job.addTask(random_forest_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(random_forest_task)
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
