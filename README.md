Description: Making a AI project just to play around and ShowCase skills. This AI is starting out basic, and will slowly work on it as the years go. This is my practice model, as I'm building this off my Phone in-between my Bash lessons.


1. Setting up Your Virtual Environment 
{
  1. ./scripts/setup_environment.sh will automate this process. First copy the file. Next create a file and paste the contents. Chmod +x the file name. To run ./setup_environment.sh. You may need to use sudo depending on your User powers.
}


2. Breakdown of the Workflow
name:
{
GuardianAI Continuous Integration: A clear, human-readable name for the workflow that will appear in the "Actions" tab on GitHub.
on:: This defines the triggers. The workflow will start automatically whenever someone pushes a commit to the main branch or opens/updates a pull_request that targets main. This is the perfect setup for quality control.

jobs:: Defines the tasks to be performed. We have one job called build-and-test.
strategy: matrix:: This is the most powerful part. Instead of writing separate workflows for each OS and Python version, the matrix tells GitHub to create a separate job for every combination. In this case, it will spin up 9 jobs (3 OS x 3 Python versions) to test our code in parallel. fail-fast: false ensures that if the tests fail on Python 3.9, the jobs for 3.10 and 3.11 will still run to completion, giving us a full picture of compatibility.
runs-on: ${{ matrix.os }}: This tells each job to use the operating system specified by the current matrix combination (e.g., ubuntu-latest).
steps:: These are the individual commands executed in order.
actions/checkout@v4: A standard action that downloads your repository's code onto the runner machine.
actions/setup-python@v5: Another standard action that installs the desired Python version. We use cache: 'pip' to save our installed packages, which makes subsequent runs much faster.
Install Dependencies: A standard shell command that upgrades pip and then installs everything from our requirements-dev.txt file. This includes pytest, black, ruff, etc.
Lint with Ruff and Black: This step runs our quality tools. ruff . checks for common errors and style issues. black --check . verifies that the code is formatted correctly without changing any files. If the code is not formatted, this step will fail, forcing the contributor to format it locally before merging.
Test with Pytest: This executes our test suite. --cov=src/guardian_ai is important; it tells the coverage tool to only report on code inside our actual package, ignoring tests and other files. --cov-report=xml generates a coverage.xml file, which is a standard format used by reporting tools.
Upload coverage reports to Codecov: This step takes the coverage.xml file and uploads it to a service like Codecov. When you link Codecov to your GitHub repo, it will post a comment in each pull request showing how test coverage has changed, which is incredibly useful. Remember to replace YourGitHubUsername/GuardianAI with your actual repository path.
How to Use This
Create the directory structure .github/workflows/ in your project root.
Save the code above as python-ci.yml inside that directory.
Commit and push this file to your GitHub repository.
That's it! The next time you open a pull request or push to main, you will see this workflow automatically start running in the "Actions" tab of your repository. It will provide a clear green checkmark for success or a red X for failure, with links to the logs for easy debugging.
This puts a professional, automated quality gate on our project. We have now established a solid foundation for development.
}

