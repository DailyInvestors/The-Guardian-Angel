# =============================================================================
# GuardianAI Environment Setup Script for Windows (PowerShell)
# =============================================================================
#
# This script automates the setup of a Python virtual environment for the
# GuardianAI project.
#
# --- IMPORTANT ---
# If you get an error about scripts being disabled on this system, you need to
# change your execution policy for this terminal session. Run this command:
#
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
#
# Then, re-run this script.
# =============================================================================

# --- Configuration ---
$VenvDir = "venv"

# --- Style and Messaging ---
$ColorHost = $Host.UI.RawUI
$SuccessColor = "Green"
$WarningColor = "Yellow"
$ErrorColor = "Red"
$InfoColor = "Cyan"

# --- Helper Function to Find Python ---
function Get-PythonCommand {
    $python_cmds = "python", "python3", "py"
    foreach ($cmd in $python_cmds) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) {
            Write-Host "✅ Python executable found as '$cmd'." -ForegroundColor $SuccessColor
            return $cmd
        }
    }
    return $null
}

# --- Main Script ---
Write-Host "🚀 Starting GuardianAI Environment Setup for Windows..." -ForegroundColor $WarningColor

# 1. Check for Python
$PythonExe = Get-PythonCommand
if (-not $PythonExe) {
    Write-Host "❌ ERROR: Python is not installed or not found in your PATH." -ForegroundColor $ErrorColor
    Write-Host "Please install Python 3.8+ and ensure it's added to your PATH."
    exit 1
}

# 2. Create the Python Virtual Environment
$ActivationScript = Join-Path -Path $VenvDir -ChildPath "Scripts\Activate.ps1"

if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating Python virtual environment in '.\$VenvDir'..." -ForegroundColor $InfoColor
    & $PythonExe -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create the virtual environment." -ForegroundColor $ErrorColor
        exit 1
    }
} else {
    Write-Host "Virtual environment '.\$VenvDir' already exists." -ForegroundColor $InfoColor
}

# 3. Activate the Virtual Environment
Write-Host "Attempting to activate the virtual environment..." -ForegroundColor $InfoColor
try {
    . $ActivationScript
    Write-Host "✅ Virtual environment activated." -ForegroundColor $SuccessColor
} catch {
    Write-Host "❌ ERROR: Failed to activate the virtual environment." -ForegroundColor $ErrorColor
    Write-Host "This is likely due to your PowerShell Execution Policy." -ForegroundColor $WarningColor
    Write-Host "To fix this, run the following command in this terminal and then re-run this script:" -ForegroundColor $WarningColor
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process" -ForegroundColor "White"
    exit 1
}

# 4. Upgrade Pip
Write-Host "Upgrading pip..." -ForegroundColor $InfoColor
pip install --upgrade pip --quiet

# 5. Install Dependencies
Write-Host "Installing all required packages from requirements-dev.txt..." -ForegroundColor $InfoColor
pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Failed to install dependencies. Please check the error messages above." -ForegroundColor $ErrorColor
    exit 1
}
Write-Host "✅ Dependencies installed successfully." -ForegroundColor $SuccessColor


# --- Final Instructions ---
Write-Host "" # Newline
Write-Host "🎉 Setup Complete! 🎉" -ForegroundColor $SuccessColor
Write-Host "The virtual environment '$VenvDir' is now active."
Write-Host "You can now run and develop GuardianAI."
Write-Host "To deactivate this environment later, simply run:" -ForegroundColor $WarningColor
Write-Host "deactivate" -ForegroundColor "White"