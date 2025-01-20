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

## Architecture Diagram
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
2. Configure the API locally. [Refer to documentation for more details].

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
