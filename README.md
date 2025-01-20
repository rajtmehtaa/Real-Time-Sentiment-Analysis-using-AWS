# Real-Time-Sentiment-Analysis-using-AWS
<h2>Project Overview</h2>
<p>This project focuses on building a robust Sentiment Analysis Pipeline using AWS services to process real-time news articles and deliver actionable insights. By integrating the Guardian API for real-time data ingestion and leveraging machine learning for sentiment analysis, the system efficiently processes and stores results in a scalable cloud-based architecture. An interactive dashboard, containerized and deployed on AWS ECS Fargate, is configured with IPv4 access, showcasing how cloud-hosted applications can be made globally accessible.</p>
<h2>Technologies Used</h2>
<p><ul>
  <li><strong>AWS Services:</strong> Lambda, EventBridge, RDS (PostgreSQL), S3, ECS Fargate, ECR</li>
  <li><strong>Guardian API:</strong> For real-time news article headings</li>
  <li><strong>Streamlit:</strong> For building the interactive visualization dashboard</li>
  <li><strong>Docker:</strong> For containerization</li>
  <li><strong>Poetry:</strong> For dependency management</li>
  <li><strong>NLTK:</strong> For sentiment analysis</li>
</ul></p>
<h2>Features</h2>
<p><ul>
<li>Automated article ingestion every 5 minutes using <stong>AWS EventBridge</stong> and <strong>Lambda.</strong></li>
<li>Sentiment analysis using <strong>NLTK's SentimentIntensityAnalyzer.</strong></li>
<li>Data stored in <strong>PostgreSQL (RDS)</strong> for querying and <strong>S3</strong> for backups.</li>
<li>An interactive <strong>Streamlit Dashboard</strong>, globally accessible via the cloud.</li>
<li>Fully containerized using <strong>Docker</strong> and deployed on <strong>ECS Fargate.</strong></li>
</ul></p>
<h2>Setup and Workflow</h2>
<p><ol>
<li><strong>Pre-Requisites</strong></li>
<ul>
  <li>AWS account configured with required IAM roles.</li>
  <li>Python installed locally.</li>
  <li>AWS CLI installed and configured.</li>
  <li>Docker installed locally.</li>
  <li>Windows Subsystem for Linux (WSL) installed and configured to enable the use of Bash commands for tasks like managing Poetry dependencies and working with Dockerfiles.</li>
</ul>
<p><li>Architecture Workflow</li></p>
<ul>
  <li><strong>Guardian API:</strong> Fetches real-time news articles.</li>
  <li><strong>AWS Lambda:</strong> Processes the articles, performs sentiment analysis, and saves the data.</li>
  <li><strong>AWS EventBridge:</strong> Triggers the AWS Lambda function every 5 minutes to automate real-time data ingestion.</li>
  <li><strong>AWS RDS (PostgreSQL):</strong> Stores processed data for structured querying and efficient retrieval.</li>
  <li><strong>S3:</strong> Stores raw data as a backup for future use and scalability.</li>
  <li><strong>Streamlit App:</strong> Provides an interactive visualization of sentiment analysis results, allowing users to explore insights easily.</li>
  <li><strong>ECS Fargate:</strong> Hosts the Streamlit app in a containerized environment, ensuring global accessibility via the cloud.</li>
</ul>
</ol></p>
<h2>Setup Instructions</h2>
<h4>Guardian API</h4>
<ul>
<li><p>Register for the Guardian API key (https://open-platform.theguardian.com/documentation/)</p></li>
<li>Configure API locally [Goto: for more information]</li>
</ul>
<h4>Postgres</h4>
Create the table with the following SQL query:
```sql
CREATE TABLE gp_analytics(
	author varchar(50),
	timestamp timestamp with time zone,
	text varchar(300),
	sentiment_score double precision,
	PRIMARY KEY(author, timestamp)
	);



