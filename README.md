# Vehicle_Insurance_Project


This repository demonstrates a full-stack machine learning pipeline—from data ingestion and preprocessing to model training, evaluation, and deployment—integrated with modern cloud services and CI/CD practices. This project is an excellent portfolio piece that highlights skills in software development, data engineering, and machine learning deployment.

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Environment Setup](#environment-setup)
3. [MongoDB Setup](#mongodb-setup)
4. [Logging & Exception Handling](#logging--exception-handling)
5. [Data Ingestion](#data-ingestion)
6. [Data Validation, Transformation & Model Trainer](#data-validation-transformation--model-trainer)
7. [AWS Integration & Model Management](#aws-integration--model-management)
8. [Model Evaluation & Pusher](#model-evaluation--pusher)
9. [Prediction Pipeline](#prediction-pipeline)
10. [CI/CD & Deployment](#cicd--deployment)
11. [How to Run](#how-to-run)
12. [Conclusion](#conclusion)

---

## Project Setup

1. **Project Template Initialization**  
   - Execute `template.py` to generate the project structure.

2. **Local Package Imports**  
   - Update `setup.py` and `pyproject.toml` to import local packages.  
   - Refer to `crashcourse.txt` for detailed guidelines.

---

## Environment Setup

1. **Virtual Environment Creation**
   ```bash
   conda create -n vehicle python=3.10 -y
   conda activate vehicle


Install Dependencies

Add required modules to requirements.txt.

Install the modules:

bash
Copy
pip install -r requirements.txt
pip list  # Verify local package installations
MongoDB Setup
MongoDB Atlas Configuration

Sign up for MongoDB Atlas and create a new project.

In the "Create a Cluster" screen, select the M0 service (free tier) with default settings and create the deployment.

Set up a database user with a username and password.

Under "Network Access", add the IP address 0.0.0.0/0 to allow connections from anywhere.

Retrieve the connection string (replace <password> with your actual password).

Demo Notebook

Create a folder named notebook.

Add your dataset to this folder.

Create a Jupyter Notebook named mongoDB_demo.ipynb, select the vehicle kernel, and use it to push data to your MongoDB Atlas database.

Verify the uploaded data by browsing the collection in MongoDB Atlas.

Logging & Exception Handling
Logger

Develop a logger file and test its functionality using demo.py.

Exception Handling

Create an exception handling file and test it with demo.py.

EDA and Feature Engineering

Include notebooks dedicated to Exploratory Data Analysis (EDA) and feature engineering.

Data Ingestion
Configuration Setup

Declare necessary variables in constants/__init__.py.

Add code in configuration/mongo_db_connections.py to define the function for establishing a MongoDB connection.

Data Access

Within the data_access folder, add code (e.g., in a file like proj1_data.py) to connect with MongoDB, fetch data in key-value format, and transform it into a DataFrame.

Entity Configuration

Update entity/config_entity.py with the DataIngestionConfig class.

Update entity/artifact_entity.py with the DataIngestionArtifact class.

Pipeline Integration

Add the necessary code in components/data_ingestion.py to integrate the ingestion process with the training pipeline.

Run demo.py to test the ingestion process (ensure the MongoDB connection URL is set as described below).

MongoDB Connection URL Setup
For Bash:

bash
Copy
export MONGODB_URL="mongodb+srv://<username>:<password>@your-cluster-url/..."
echo $MONGODB_URL
For PowerShell:

powershell
Copy
$env:MONGODB_URL = "mongodb+srv://<username>:<password>@your-cluster-url/..."
echo $env:MONGODB_URL
For Windows Environment Variables:

Set the MONGODB_URL variable through the system environment settings.

Note: Remember to add the "artifact" directory to your .gitignore file.

Data Validation, Transformation & Model Trainer
Data Validation

Update src/utils/main_utils.py with the necessary utility functions.

Complete the config/schema.yaml with the full dataset schema.

Develop the Data Validation component similar to the Data Ingestion component.

Data Transformation

Build the Data Transformation component.

Incorporate transformation logic (e.g., in entity/estimator.py).

Model Trainer

Extend entity/estimator.py with a class dedicated to model training.

AWS Integration & Model Management
AWS Services Setup

Log in to the AWS Console and set the region to us-east-1.

Create a new IAM user (e.g., firstproj) with AdministratorAccess.

Generate AWS access keys and set them as environment variables:

Bash:

bash
Copy
export AWS_ACCESS_KEY_ID="your_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
PowerShell:

powershell
Copy
$env:AWS_ACCESS_KEY_ID="your_key_id"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
Update the AWS-related constants in constants/__init__.py:

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02

MODEL_BUCKET_NAME = "my-model-mlopsproj"

MODEL_PUSHER_S3_KEY = "model-registry"

S3 Bucket Setup

In AWS S3, create a bucket named my-model-mlopsproj in the us-east-1 region.

Uncheck "Block all public access" and acknowledge the warning.

AWS S3 Integration

Add code in the src/aws_storage directory to manage S3 configurations for pushing and pulling models.

Create entity/s3_estimator.py for functions that interact with AWS S3.

Model Evaluation & Pusher
Model Evaluation

Develop a component to evaluate model performance.

Model Pusher

Implement a module to automate the process of pushing models to AWS S3.

Prediction Pipeline
Application Setup

Develop the code structure for the Prediction Pipeline.

Set up app.py as the entry point for the web application.

Create static and templates directories for static assets and HTML templates.

Routing and Deployment

Define routes (e.g., a /training route for triggering model training) in your application.

CI/CD & Deployment
Containerization & CI/CD Pipeline

Create a Dockerfile and a .dockerignore file for building your Docker image.

Set up the CI/CD pipeline by adding an AWS configuration file (aws.yaml) inside the .github/workflows directory.

Configure GitHub Actions for automated testing, building, and deployment.

EC2 Deployment

Launch an Ubuntu EC2 instance (e.g., vehicledata-machine with a T2 Medium instance type).

Install Docker on EC2:

bash
Copy
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
GitHub Runner Setup

Create a self-hosted GitHub runner and follow the instructions to configure it on your EC2 instance.

Verify that the runner appears as "idle" on GitHub.

GitHub Secrets

Set up the following secrets in your GitHub repository:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_DEFAULT_REGION

ECR_REPO

Security Group Configuration

Update your EC2 instance's security group to allow inbound traffic on port 5080.

Deployment Verification

Access the deployed application by entering <EC2_PUBLIC_IP>:5080 in your browser.

How to Run
Local Execution:
Run demo.py to execute the full training and deployment pipeline.

Model Training:
Use the /training route in the web application to trigger model training.

CI/CD Pipeline:
On every commit and push, the CI/CD pipeline will automatically build and deploy your application.

