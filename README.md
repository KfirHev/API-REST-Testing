# API-REST-Testing

![image](https://github.com/user-attachments/assets/f49972e6-4dd9-4d6e-a488-a8ab7d70b7c8)

# API Testing Framework with Python, pytest, Selenium, and Locust

An API testing framework simulating a bank account environment using **Parasoft Parabank** and **HSQDB**.  
This project includes **functional**, **negative**, and **performance tests**, leveraging **Docker** for seamless execution of the "parasoft/parabank:latest" container.  
**Locust** is used for performance testing, while **pytest** is utilized for running and managing test cases.  
With a focus on modularity and scalability, the framework is designed to support comprehensive API testing and can be easily extended for other web-based applications.

## Project Structure
```
API-REST-Testing/
|
├── .venv/
|    Python virtual environment (git ignored)
|
├── browserdriver/
|   WebDriver executables for supported browsers
|
├── libs/
|   Additional libraries for the project
|
├── Logs/
|   Folder for runtime log files (git ignored)
|
├── PageObjects/
|   Page classes with locators and actions
|
├── Reports/
|   HTML test reports with embedded screenshots (git ignored)
|
├── TEMP/
|   Temporary files (usage unspecified)
|
├── Templates/
|   Templates for test creation
|
├── Tests/  Organized test scripts
|  |
│  ├── Functional/
|  |   Functional test cases
|  |
│  ├── Integration/ 
|  |   Integration test cases
|  |
│  ├── Negative/ 
|  |   Negative test cases
|  |
│  ├── Performance/
|  |   Performance test cases and locust files
|  |
│  └── bank_api_swagger.yaml 
|     Swagger API definition for performance testing
|
├── Utils/
|   Utility files and base classes
|
├── conftest.py
|    pytest configuration
|
├──Dockerfile_all_in_one 
|  Docker configuration for all-in-one setup
│
├── Dockerfile_python
|   Docker configuration for Python-specific setup
|
├── .dockerignore
|   Files to exclude from Docker builds
|
├── .gitignore
|    Files to exclude from Git
|
├── README.md
|   Project documentation
|
└── requirements.txt # Python dependencies for the project
```
---
**🚩Note:** The `Logs/`, `Reports/`, and `Screenshots/` directories are git ignored due to the frequent generation of files that are not necessary for version control.


## Getting Started

![image](https://github.com/user-attachments/assets/d6de4289-3562-4c95-a937-c58ae0a19253)


**Example ETE test**


### 🛠 Prerequisites
- **Python 3.7 or higher**  (Locust dependency)
- **Selenium WebDriver**  
- **parasoft/parabank:latest Docker**
- **Python Docker** (optional, for pytest containerized tests)  

### Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/KfirHev/API-REST-Testing.git
    ```

2. Navigate into the project directory:
    ```bash
    cd API-REST-Testing
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

**Example run via PyCharm**

Add video 

### Running Tests

1. **To run tests from the command line using Python's virtual environment**:
   - First, activate the virtual environment by running `. \YourProjectName\.venv\Scripts\activate`.
   - Then, execute the tests by typing `pytest`. (For customization options, refer to the options section below.)

2. **To run tests in a Docker container**:
   - Build the Docker image and run the container.

**Customizable Options**:
- Use `--browser_type` to specify the browser (default is chrome; other options include firefox and edge).
- Use `--run_env` to choose the environment (default is local; you can also select docker).

### View Reports


https://github.com/user-attachments/assets/c686d899-91cc-4702-9b9a-3215943d28af


#### HTML Reports

1. Browse to the project Reports folder and choose the report ,you can drag and drop it to any browser to view it.

2. The HTML report name represent the date & time of the run.

3. The report include all the run data for each test case and their status

4. Upon failure the report will include the screenshot when it failed and the specific error logs

#### Jenkins Reports 

1. Access Jenkins: Open your Jenkins instance and navigate to the project for which the tests were executed.

2. View Report in Jenkins:
 - Locate the “Build History” section and select the specific build you want to analyze.
 - Inside the build details, you can find links to test reports, typically labeled as “Test Results” or under “HTML Publisher Plugin” if configured.
3. Detailed Test Analysis: The Jenkins report displays test statuses, including any test failures, along with logs. You’ll also see an option to view error screenshots and logs for failed tests if configured to save these artifacts.
4. Trend Analysis: Jenkins provides a view of historical test data, helping track trends in test pass/fail rates over time, enabling insights into project quality and stability.
   
     ![image](https://github.com/user-attachments/assets/14e6db20-42f4-4823-a63d-b67cf055fb84)

## Planned Enhancements

Future updates will aim to extend the functionality and robustness of this framework, with potential additions including:

- Detailed README updates, including Docker command instructions ,setting up Jenkins job/pipeline and example screenshots for a clearer demo experience
- Adding negatvie test (failures 5XX 4XX) 
- Adding mock container for simulation of edge cases (network traffic delay) using WireMock container / service (TBD)
- Adding locust stress files
- Add the recovery instructions for DB corruption
- Add Locust reports example

## Contributing

This project is designed for demonstration purposes and is currently set as read-only for showcasing the framework’s capabilities. Contributions are not open at this time, but feel free to explore and use the code as a reference for similar projects.

