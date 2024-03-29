# ProActive Python Client

![License BSD](https://img.shields.io/badge/License-BSD-blue.svg "License BSD")
![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg "Python 3")
![Proactive](https://img.shields.io/pypi/v/proactive.svg "Proactive")
[![Documentation Status](https://readthedocs.org/projects/proactive-python-client/badge/?version=latest)](https://proactive-python-client.readthedocs.io/en/latest/?badge=latest)

The ProActive Python Client enables seamless interaction with the ProActive Scheduler and Resource Manager, facilitating the automation of workflow submission and management tasks directly from Python.

## Key Features

- **Ease of Use**: Simple API for interacting with the ProActive Scheduler.
- **Workflow Management**: Submit, monitor, and manage your ProActive workflows.
- **Resource Management**: Leverage the Resource Manager for efficient computing resource allocation.

## Getting Started

### Prerequisites

- Python version 3.5 or later is required.
- Java 8 SDK

### Installation

You can easily install the ProActive Python Client using pip:

```bash
pip install --upgrade proactive
```

For access to the latest features and improvements, install the pre-release version:

```bash
pip install --upgrade --pre proactive
```

### Building from Source

#### Linux or Mac

To build and install the package from source:

```bash
# Build the package
make clean_build
# or use gradlew
gradlew clean build

# Install the built package
pip install dist/proactive-XXX.zip  # Replace XXX with the actual version
```

#### Windows

```bat
REM Build the package
build.bat CLEAN_BUILD

REM Install the built package
REM Replace XXX with the actual version
pip install dist\proactive-XXX.zip
```

### Running Tests

#### With Gradle

Specify your ProActive credentials and run the tests:

```bash
./gradlew clean build -Pproactive_url=YOUR_URL -Pusername=YOUR_USERNAME -Ppassword=YOUR_PASSWORD
```

#### With Make

First, create a `.env` file with your ProActive credentials:

```ini
PROACTIVE_URL=YOUR_URL
PROACTIVE_USERNAME=YOUR_USERNAME
PROACTIVE_PASSWORD=YOUR_PASSWORD
```

Then execute:

```bash
make test
```

## Quickstart Example

This simple example demonstrates connecting to a ProActive server, creating a job, adding a Python task, and submitting the job:

```python
import os
import getpass
from proactive import ProActiveGateway

proactive_url = "https://try.activeeon.com:8443"

print(f"Connecting to {proactive_url}...")
gateway = ProActiveGateway(proactive_url)

# Securely input your credentials
gateway.connect(username=input("Username: "), password=getpass.getpass("Password: "))
assert gateway.isConnected(), "Failed to connect to the ProActive server!"

# Job and task creation
print("Creating and configuring a ProActive job and task...")
proactive_job = gateway.createJob()
proactive_job.setJobName("SimpleJob")

proactive_task = gateway.createPythonTask("SimplePythonTask")
proactive_task.setTaskImplementation('print("Hello from ProActive!")')
proactive_task.addGenericInformation("PYTHON_COMMAND", "python3")
proactive_job.addTask(proactive_task)

# Job submission
job_id = gateway.submitJob(proactive_job)
print(f"Job submitted with ID: {job_id}")

# Retrieve job output
print("Job output:")
print(gateway.getJobOutput(job_id))

# Cleanup
gateway.disconnect()
gateway.terminate()
print("Disconnected and finished.")
```

## Documentation

For more detailed usage and advanced functionalities, please refer to the [ProActive Python Client Documentation](https://proactive-python-client.readthedocs.io/en/latest/).

## Examples Repository

For practical examples showcasing various features of the ProActive Python Client, visit our [examples repository](https://github.com/ow2-proactive/proactive-python-client-examples).

## Contributing

Contributions are welcome! If you have an improvement or a new feature in mind, feel free to fork the repository, make your changes, and submit a pull request.
