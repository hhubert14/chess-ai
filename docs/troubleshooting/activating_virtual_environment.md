# Activating Virtual Environment

To activate a Python virtual environment (venv) on Windows, follow these steps:
1. First, create a virtual environment if you haven't already:
    ```bash
    python -m venv path\to\venv_name
    ```
2. To activate the virtual environment:
    - In Command Prompt (cmd):
        ```bash
        path\to\venv_name\Scripts\activate.bat
        ```
    - In PowerShell:
        ```bash
        path\to\venv_name\Scripts\Activate.ps1
        ```
3. To deactivate the virtual environment when you're done:
    ```bash
    deactivate
    ```