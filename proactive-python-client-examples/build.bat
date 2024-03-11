@echo off
setlocal

echo Received argument: %1

set PYTHON_SDK_HOME=\PATH_TO\proactive-python-client
set PYTHON=python

if "%1"=="SETUP_VENV" goto SETUP_VENV
if "%1"=="VIRTUAL_ENV" goto VIRTUAL_ENV
if "%1"=="UNINSTALL_PROACTIVE" goto UNINSTALL_PROACTIVE
if "%1"=="INSTALL_LATEST" goto INSTALL_LATEST
if "%1"=="INSTALL_LATEST_TEST" goto INSTALL_LATEST_TEST
if "%1"=="INSTALL_LATEST_LOCAL" goto INSTALL_LATEST_LOCAL
if "%1"=="RUN_ALL" goto RUN_ALL
if "%1"=="PRINT_VERSION" goto PRINT_VERSION
if "%1"=="HELP" goto HELP
echo Invalid command. Use "build.bat HELP" for a list of available commands.
goto :EOF

:SETUP_VENV
echo Setting up virtual environment...
%PYTHON% -m venv env
call env\Scripts\activate.bat && %PYTHON% -m pip install --upgrade pip setuptools python-dotenv
call env\Scripts\activate.bat && %PYTHON% -m pip -V
echo Virtual environment is ready.
goto :EOF

:VIRTUAL_ENV
if exist "env\" (
    echo Virtual environment already exists.
    set /p answer="Do you want to delete it and create a new one? [y/N] "
    if /I "%answer%"=="y" (
        echo Deleting and recreating the virtual environment...
        rmdir /s /q env
        call :SETUP_VENV
    ) else (
        echo Using the existing virtual environment.
    )
) else (
    call :SETUP_VENV
)
goto :EOF

:UNINSTALL_PROACTIVE
echo Uninstalling proactive package...
call env\Scripts\activate.bat && %PYTHON% -m pip uninstall -y proactive
echo Proactive package uninstalled.
goto :EOF

:INSTALL_LATEST
echo Installing the latest pre-release of proactive...
call env\Scripts\activate.bat && %PYTHON% -m pip install --upgrade --pre proactive
echo Latest pre-release of proactive installed.
goto :EOF

:INSTALL_LATEST_TEST
echo Installing the latest test version of proactive from TestPyPI...
call env\Scripts\activate.bat && %PYTHON% -m pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --pre proactive
echo Latest test version of proactive installed.
goto :EOF

:INSTALL_LATEST_LOCAL
echo Installing the latest local version of proactive...
call env\Scripts\activate.bat
for %%z in (%PYTHON_SDK_HOME%\dist\*.zip) do (
    %PYTHON% -m pip install "%%z"
)
echo Latest local version of proactive installed.
goto :EOF

:RUN_ALL
echo Running all Python scripts...
call env\Scripts\activate.bat
for %%f in (*.py) do (
    echo Running %%f...
    %PYTHON% %%f
)
echo All Python scripts have been run.
goto :EOF

:PRINT_VERSION
call env\Scripts\activate.bat && %PYTHON% -m pip show proactive
call env\Scripts\activate.bat && %PYTHON% -c "import proactive; print(proactive.__version__)"
goto :EOF

:HELP
echo Usage: build.bat [command]
echo Available commands: SETUP_VENV VIRTUAL_ENV UNINSTALL_PROACTIVE INSTALL_LATEST INSTALL_LATEST_TEST INSTALL_LATEST_LOCAL RUN_ALL PRINT_VERSION
goto :EOF
