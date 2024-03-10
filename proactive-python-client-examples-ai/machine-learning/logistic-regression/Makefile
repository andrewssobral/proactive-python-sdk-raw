.PHONY: virtualenv setup_venv uninstall_proactive install_latest install_latest_test install_latest_local submit run_all help

PYTHON_SDK_HOME="/PATH_TO/proactive-python-client"
PYTHON=python3

setup_venv:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv env
	@. env/bin/activate && $(PYTHON) -m pip install --upgrade pip setuptools
	@. env/bin/activate && $(PYTHON) -m pip install -r requirements.txt
	@. env/bin/activate && $(PYTHON) -m pip -V
	@echo "Virtual environment is ready."

virtualenv:
	@if [ -d "env" ]; then \
		echo "Virtual environment already exists."; \
		read -p "Do you want to delete it and create a new one? [y/N] " answer; \
		case $$answer in \
			[Yy]* ) \
				echo "Deleting and recreating the virtual environment..."; \
				rm -rf env; \
				$(MAKE) setup_venv;; \
			* ) \
				echo "Using the existing virtual environment.";; \
		esac \
	else \
		$(MAKE) setup_venv; \
	fi

uninstall_proactive:
	@echo "Uninstalling proactive package..."
	@. env/bin/activate && $(PYTHON) -m pip uninstall -y proactive
	@echo "Proactive package uninstalled."

install_latest: uninstall_proactive
	@echo "Installing the latest pre-release of proactive..."
	@. env/bin/activate && $(PYTHON) -m pip install --pre proactive
	@echo "Latest pre-release of proactive installed."

install_latest_test: uninstall_proactive
	@echo "Installing the latest test version of proactive from TestPyPI..."
	@. env/bin/activate && $(PYTHON) -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --pre proactive
	@echo "Latest test version of proactive installed."

install_latest_local: uninstall_proactive
	@echo "Installing the latest local version of proactive..."
	@. env/bin/activate; for zip in $(PYTHON_SDK_HOME)/dist/*.zip; do \
		python -m pip install "$$zip"; \
	done
	@echo "Latest local version of proactive installed."

run_all:
	@echo "Running all Python scripts..."
	@. env/bin/activate && for file in *.py; do \
		echo "Running $$file..."; \
		$(PYTHON) $$file; \
	done
	@echo "All Python scripts have been run."

submit:
	@echo "Running submit2proactive script..."
	@. env/bin/activate && $(PYTHON) submit2proactive.py
	@echo "Done."

help:
	@cat Makefile
