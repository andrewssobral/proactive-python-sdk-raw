# Proactive Python Client Examples

This repository contains a collection of example scripts that demonstrate various features of the proactive Python client. These scripts showcase how to create and manage jobs, tasks, and use advanced scheduling features in a Python environment.

## Setting Up the Environment

Before running the examples, you may want to create a virtual environment to avoid conflicts with other Python projects. A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages.

### Creating a Virtual Environment (Optional)

#### On Mac and Linux

To create a virtual environment, run the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

You can also use the provided `Makefile`:
```bash
make virtualenv
```

#### On Windows

On Windows, you can use the provided `build.bat` script to create and manage the virtual environment:

```cmd
build.bat VIRTUAL_ENV
```

This command will create a new virtual environment or use the existing one based on your input.

### Upgrading Required Packages

Once the virtual environment is activated, upgrade `pip`, `setuptools` and `python-dotenv` to the latest versions:

#### On Mac and Linux

```bash
python3 -m pip install --upgrade pip setuptools python-dotenv
```

If you have used the provided `Makefile`, it automatically upgrades these packages when setting up the virtual environment.

#### On Windows

The `build.bat` script automatically upgrades these packages when setting up the virtual environment.

## Installing the Proactive Python SDK

To install the latest pre-release or development version of the Proactive Python SDK, which includes the most recent features and fixes, use the following command:

```bash
python3 -m pip install --upgrade --pre proactive
```

The `--pre` flag is included to allow pip to find and install pre-releases.

#### Using Makefile (For Mac and Linux)

```bash
make install_latest
```

#### On Windows

```cmd
build.bat INSTALL_LATEST
```

## Running the Examples

To test if the installation was successful and see the proactive client in action, you can run the provided example scripts. For instance, to run the `demo_basic.py` script:

```bash
python3 demo_basic.py
```

#### Using Makefile (For Mac and Linux)

For instance, to run all the provided example scripts:

```bash
make run_all
```

#### On Windows

To run all the provided example scripts:

```cmd
build.bat RUN_ALL
```

This command will execute all `.py` files in the current directory.

## Examples Description

- `demo_basic.py`: A simple script that showcases how to connect to the ProActive Scheduler, create a job and a Python task, and execute it.

- `demo_impl_file.py`: Demonstrates the basic usage of the ProActive Scheduler for executing a Python task implemented in an external file.

- `demo_exec_file.py`: This advanced script runs a Python task from a file with input files, pre-scripts, and post-scripts. It highlights the ability to execute complex scripts with external dependencies.

- `demo_transf_file.py`: Demonstrates file handling in ProActive tasks, focusing on including input files for processing and designating output files to capture task results. This script counts the number of files in a specified directory and outputs the count both to the terminal and to a file within the same directory, showcasing data transfer and file management in ProActive workflows.

- `demo_forkenv.py`: Shows how to create and execute a Python task within a job, with emphasis on configuring the execution environment using a fork environment script.

- `demo_selectionscript.py`: This script explains how to create a job and a task, and ensures that the task is executed only on Linux machines using a selection script.

- `demo_impl_url.py`: Illustrates how to set up a machine learning task (Logistic Regression) using a script sourced from a URL, showing the ProActive Scheduler's capability to incorporate external scripts.

- `demo_job_status.py`: Demonstrates the process of job submission and monitoring with the ProActive Python SDK. It walks through creating a job, adding a Python task, submitting the job to the ProActive Scheduler, and monitoring its status until completion, concluding with the retrieval and display of the job's output.

- `demo_ai_workflow.py`: Sets up and executes a machine learning workflow for the Iris dataset using the ProActive Scheduler. It demonstrates how to create a job, add tasks, and manage their execution sequence.

Please ensure the ProActive Scheduler is running and accessible, and that you have the required scripts and environments set up before executing these examples.

## Advanced Examples

The repository also includes a collection of advanced examples that demonstrate more complex use cases of the ProActive Scheduler, particularly focusing on machine learning workflows. These examples illustrate how to set up, configure, and execute sophisticated machine learning models and workflows using the ProActive Python client.

### Machine Learning Workflows

- **Diabetics Detection**: Utilizes various machine learning algorithms to detect diabetic patients from clinical datasets.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_AutoSklearn_Classifier`: Detects diabetes using the Auto-sklearn Classifier.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_Isolation_Forest`: Applies Isolation Forest for anomaly detection in diabetes data.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_K_Means`: Employs K-Means clustering for diabetes data segmentation.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_Mean_Shift`: Uses Mean Shift clustering for diabetes data analysis.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_One_Class_SVM`: Implements One-Class SVM for outlier detection in diabetes datasets.
  - `python -m demo_ai_workflows.Diabetics_Detection_Using_TPOT_Classifier`: Leverages the TPOT Classifier for automated machine learning in diabetes detection.

- **House Price Prediction**: Demonstrates the use of various regression models to predict house prices based on the Boston housing dataset.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_AutoSklearn_Regressor`: Predicts house prices using Auto-sklearn Regressor.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Bayesian_Ridge_Regression`: Applies Bayesian Ridge Regression for house price prediction.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Linear_Regression`: Utilizes Linear Regression for predicting house prices.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_Support_Vector_Regression`: Employs Support Vector Regression for house price estimation.
  - `python -m demo_ai_workflows.House_Price_Prediction_Using_TPOT_Regressor`: Uses the TPOT Regressor for automated machine learning in house price prediction.

- **Iris Flowers Classification**: Showcases classification models for identifying Iris flower species from the Iris dataset.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_AdaBoost`: Classifies Iris species using AdaBoost.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_CatBoost`: Implements CatBoost for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Gaussian_Naive_Bayes`: Utilizes Gaussian Naive Bayes for classifying Iris species.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Gradient_Boosting`: Applies Gradient Boosting for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Logistic_Regression`: Uses Logistic Regression for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Random_Forest`: Employs Random Forest for classifying Iris species.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_Support_Vector_Machines`: Demonstrates SVM usage for Iris species classification.
  - `python -m demo_ai_workflows.Iris_Flowers_Classification_Using_XGBoost`: Leverages XGBoost for Iris species classification.

### In-Depth Example: CIFAR-10 Logistic Regression Classifier

The [CIFAR-10 Logistic Regression Classifier](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) example demonstrates how to train and evaluate a logistic regression model on the CIFAR-10 dataset, which is a common benchmark in machine learning for image classification tasks.

- **Repository Contents**: The repository includes:

- Scripts for training and evaluating the model (`train.py` and `eval.py`).
- A directory structure to organize models and predictions.
- A sample script (`submit2proactive.py`) to submit a job to the ProActive Scheduler, showing how to run complex machine learning workflows on distributed computing environments.

- **Getting Started**: To explore this advanced example, visit the [repository](https://github.com/ow2-proactive/ai-examples/tree/master/machine-learning/logistic-regression) and follow the instructions provided in its `README` to set up your environment, train the model, and submit the job to ProActive.

Please ensure that your environment meets the prerequisites and that the ProActive Scheduler is running and accessible before you begin.

## Additional Information

- Ensure you have Python 3.6 or later to use the proactive client.
- If you encounter any issues, please report them on the [Issues](https://github.com/ow2-proactive/proactive-python-client-examples/issues) page.
- For more information about the proactive client, refer to the [official documentation](https://github.com/ow2-proactive/proactive-python-client).

## Contributing

We welcome contributions to this repository. If you have an improvement or a new example, please fork the repository, make your changes, and submit a pull request.
