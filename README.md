# Real-Time Sentiment Analysis using AWS

## Project Overview
This project focuses on building a robust Sentiment Analysis Pipeline using AWS services to process real-time news articles and deliver actionable insights. By integrating the Guardian API for real-time data ingestion and leveraging machine learning for sentiment analysis, the system efficiently processes and stores results in a scalable cloud-based architecture. An interactive dashboard, containerized and deployed on AWS ECS Fargate, is configured with IPv4 access, showcasing how cloud-hosted applications can be made globally accessible.

---

## Technologies Used
- **AWS Services**: Lambda, EventBridge, RDS (PostgreSQL), S3, ECS Fargate, ECR
- **Guardian API**: For real-time news article headings
- **Streamlit**: For building the interactive visualization dashboard
- **Docker**: For containerization
- **Poetry**: For dependency management
- **NLTK**: For sentiment analysis

---

## Features
- Automated article ingestion every 5 minutes using **AWS EventBridge** and **Lambda**.
- Sentiment analysis using **NLTK's SentimentIntensityAnalyzer**.
- Data stored in **PostgreSQL (RDS)** for querying and **S3** for backups.
- An interactive **Streamlit Dashboard**, globally accessible via the cloud.
- Fully containerized using **Docker** and deployed on **ECS Fargate**.

---

## Setup and Workflow

### Architecture Diagram
![Image](https://github.com/user-attachments/assets/a7eeaf45-423a-4afa-8a8d-84f2c641ecd7)

### Pre-Requisites
- AWS account configured with required IAM roles.
- Python installed locally.
- AWS CLI installed and configured.
- Docker installed locally.
- Windows Subsystem for Linux (WSL) installed and configured to enable the use of Bash commands for tasks like managing Poetry dependencies and working with Dockerfiles.

### Architecture Workflow
- **Guardian API**: Fetches real-time news articles.
- **AWS Lambda**: Processes the articles, performs sentiment analysis, and saves the data.
- **AWS EventBridge**: Triggers the AWS Lambda function every 5 minutes to automate real-time data ingestion.
- **AWS RDS (PostgreSQL)**: Stores processed data for structured querying and efficient retrieval.
- **S3**: Stores raw data as a backup for future use and scalability.
- **Streamlit App**: Provides an interactive visualization of sentiment analysis results, allowing users to explore insights easily.
- **ECS Fargate**: Hosts the Streamlit app in a containerized environment, ensuring global accessibility via the cloud.

---

## Setup Instructions

### Guardian API
1. Register for the Guardian API key: [Guardian API Documentation](https://open-platform.theguardian.com/documentation/)

### Postgres
Create the table with the following SQL query:

```sql
CREATE TABLE gp_analytics(
    author varchar(50),
    timestamp timestamp with time zone,
    text varchar(300),
    sentiment_score double precision,
    PRIMARY KEY(author, timestamp)
);
```
### S3 Bucket
Create an S3 bucket to store raw article data

### Lambda Function
- Use the provided lambda_function.py to fetch articles, perform sentiment analysis, and store the results in RDS and S3.
- To Simplify the deployment and avoid including large libraries directly in the Lambda function, we have to use **AWS Lammbda k-Layers** for pre-installed dependencies.
- Paste the ARNs for the respective layers based on your AWS Region.
    - arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-nltk:47
    - arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pytz:5
    - arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-python38-pandas:37
- Configure the environment variables for the kLayers
    - `GUARDIAN_API_KEY`
    - `DB_HOST`
    - `DB_PASSWORD`
    - `S3_BUCKET_NAME`
      
### Schedule Lambda with EventBridge
Configure AWS EventBridge to trigger the Lambda function every 5 minutes.

### The Streamlit App
Use Streamlit to visualize sentiment analysis results with color-coded sentiment scores (red for negative, green for positive, and gray for neutral). Refer to xyz.py for the Streamlit implementation.

### Manage Dependencies with Poetry and Containerize the Streamlit App
- Refer Local Setup on how to install and manage dependencies using Poetry and Building and Testing the Docker Image.

### Deploy on ECS Fargate
- Use the AWS CLI to upload the containerized Streamlit app to Amazon Elastic Container Registry (ECR)
- Create an ECS Fargate Cluster and define a task definiation that uses the Docker image from your ECR Repository, and set the required Environment variables.
- After deploying the App, Configure the IPv4 for Public Access. Ensure that the ECS Fargate task has a public IPv4 address assigned. The default port will be 8501 for IPv4.

## Local Setup
For running this locally, it would be better to run the code by creating a conda virtual environment and install the following:
- Install anaconda3
- Start Anaconda Powershell
- set the environment variables:
```bash
[Environment]::SetEnvironmentVariable("GUARDIAN_API_KEY", "Your-api-key", "User")
[Environment]::SetEnvironmentVariable("S3_BUCKET_NAME", "my-guardianpost-analytics-storage", "User")
[Environment]::SetEnvironmentVariable("DB_PASSWORD", "password", "User")
[Environment]::SetEnvironmentVariable("DB_HOST", "your-RDS-endpoint", "User")
```

```bash
conda create --name guardianpost_analytics_py38 python=3.8 spyder
conda activate guardianpost_analytics_py38
conda install -c conda-forge poetry # dependency management
conda install -c conda-forge notebook # for jupyter
```

- For Install Project Dependencies
```bash
poetry install
```   

- After setting up the Environment variables you can run the Dashboard locally with:
```bash
poetry run streamlit run src/app.py
```   

## Screenshot
#### Dashboard with color-coded sentiment scores.
![Image](https://github.com/user-attachments/assets/ed572b83-4c3c-4d6f-8e95-da12a78c6faf)

