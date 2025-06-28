GuardianAI 🛡️
![alt text](https://github.com/DailyInvestors/GuardianAI/actions/workflows/python-ci.yml/badge.svg)

![alt text](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

![alt text](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue.svg)
GuardianAI is a community-driven, open-source project to build a powerful, transparent, and accessible multimodal AI for security analysis. Our mission is to create a tool that can understand not just code and text-based threat reports, but also visual data like screenshots of phishing attempts, to provide a more holistic approach to digital security.
Key Features
🧠 Multimodal by Design: Analyzes text (code, CVEs, reports), and images (website screenshots, logos) to identify threats.
🔐 Security-Focused: Trained on a specialized corpus of vulnerable code, security advisories, threat intelligence reports, and phishing data.
📖 Open & Transparent: All code, training data processing scripts, and model architectures are open-source to encourage trust, collaboration, and verification.
🧩 Modular Architecture: Built with a clean, component-based structure in PyTorch, making it easy for contributors to improve specific parts of the model.
🤝 Community-Driven: GuardianAI's strength comes from its community. We welcome contributions of all kinds, from data curation to model development.
Getting Started: Installation
Follow these steps to set up your local development environment.
Prerequisites
Git: You must have Git installed to clone the repository. Download Git.
Python: You need Python 3.9, 3.10, or 3.11. Download Python.
Important: During installation, make sure to check the box that says "Add Python to PATH" or similar.
Core Setup Steps
First, clone the repository to your local machine:
Generated sh
git clone https://github.com/YourUsername/GuardianAI.git
cd GuardianAI
Use code with caution.
Sh
Replace YourUsername with the actual GitHub organization or username.
Now, follow the instructions for your specific operating system.
💻 For Windows (Microsoft)
We use PowerShell to set up the environment on Windows.
Open PowerShell: Open a PowerShell terminal (do not use Command Prompt/CMD).
Adjust Execution Policy (If Needed): By default, PowerShell may block script execution. Run the following command to allow scripts for your current session. This is a safe, temporary change.
Generated powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
Use code with caution.
Powershell
Run the Setup Script:
Generated powershell
.\scripts\setup_environment.ps1
Use code with caution.
Powershell
This script will create a venv, activate it, and install all necessary dependencies.
🍎 For macOS (Apple) & 🐧 For Linux (including ChromeOS)
For macOS, Linux, and the Linux environment on ChromeOS, we use the Bash setup script.
Open your Terminal.
Make the Script Executable: This is a one-time command to grant permission to run the script.
Generated sh
chmod +x scripts/setup_environment.sh
Use code with caution.
Sh
Run the Setup Script:
Generated sh
./scripts/setup_environment.sh
Use code with caution.
Sh
This will create and configure the Python virtual environment and install all dependencies.
📱 A Note on Mobile Platforms (Android & iOS)
The GuardianAI development environment is designed for desktop operating systems (Windows, macOS, Linux). The tools required for training and developing a large AI model (PyTorch, GPU drivers, etc.) are not available on Android or iOS.
However, a long-term goal for the GuardianAI project is to make the trained model accessible to mobile applications, likely through an API. This would allow a future Android or iOS app to send data (like a suspicious URL or a screenshot) to the GuardianAI model for analysis and receive a result.
TL;DR: You develop GuardianAI on a desktop, but one day it could power security tools on your phone.
Usage
After running the setup script, your virtual environment (venv) will be active.
Running Tests
To ensure everything is working correctly, run our full test suite using pytest:
Generated sh
pytest
Use code with caution.
Sh
Code Style & Linting
We use black for code formatting and ruff for linting.
Generated sh
# To automatically format all code to match the project style
black .

# To check for potential errors and style issues
ruff .
Use code with caution.
Sh
Our Continuous Integration (CI) will fail if the code is not formatted or if ruff finds errors.
Project Structure
Here is a brief overview of the project's layout:
Generated code
/GuardianAI/
├── .github/          # GitHub-specific workflows (CI)
├── configs/          # Configuration files for models and training
├── data/             # Scripts and instructions for handling datasets (data is gitignored)
├── docs/             # Project documentation
├── evaluation/       # Scripts and benchmarks for evaluating model performance
├── notebooks/        # Jupyter notebooks for experimentation and analysis
├── scripts/          # Helper scripts (like environment setup)
├── src/guardian_ai/  # The main Python source code for the project
└── tests/            # The test suite for our source code
Use code with caution.
Contributing
We welcome contributions of all kinds! Whether you're a data scientist, a software engineer, a security researcher, or just an enthusiastic user, you can help.
Please read our CONTRIBUTING.md (coming soon!) for details on our code of conduct and the process for submitting pull requests.
For major changes, please open an issue first to discuss what you would like to change.
Join our community on Discord to chat with developers and get involved!
License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
37.3s
Start typing a prompt

