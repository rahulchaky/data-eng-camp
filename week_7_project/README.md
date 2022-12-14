## Course Project

The goal of this project is to apply everything we learned
in this course and build an end-to-end data pipeline.

### Problem statement

For the project, we will ask you to build a dashboard with two tiles. 

For that, you will need:

* Select a dataset that you're interested in (see [datasets.md](datasets.md))
* Create a pipeline for processing this dataset and putting it to a datalake
* Create a pipeline for moving the data from the lake to a data warehouse
* Transform the data in the data warehouse: prepare it for the dashboard
* Create a dashboard



## Data Pipeline 

The pipeline could be stream or batch: this is the first thing you'll need to decide 

* If you want to consume data in real-time and put them to data lake - go with stream.
* If you want to run things periodically (e.g. hourly/daily), go with batch


## Technologies 

You don't have to limit yourself to technologies covered in the course. You can use alternatives as well:

* Cloud: AWS, GCP, Azure or others
* Infrastructure as code (IaC): Terraform, Pulumi, Cloud Formation, ...
* Workflow orchestration: Airflow, Prefect, Luigi, ...
* Data Wareshouse: BigQuery, Snowflake, Redshift, ...
* Batch processing: Spark, Flink, AWS Batch, ...
* Stream processing: Kafka, Pulsar, Kinesis, ...

If you use something that wasn't covered in the course, 
be sure to explain what the tool does.

If you're not certain about some tools, ask in Slack.


## Dashboard

You can build a dashboard with any of the tools shown in the course (Data Studio or Metabase) or any other BI tool of your choice. If you do use another tool, please specify and make sure that the dashboard is somehow accessible to your peers. 

Your dashboard should contain at least two tiles, we suggest you include:

- 1 graph that shows the distribution of some categorical data 
- 1 graph that shows the distribution of the data across a temporal line

Make sure that your graph is clear to understand by adding references and titles. 

Example of a dashboard: ![image](https://user-images.githubusercontent.com/4315804/159771458-b924d0c1-91d5-4a8a-8c34-f36c25c31a3c.png)

## Going the extra mile 

If you finish the project and you want to improve it, here are a few things you can do:

* Add tests
* Use make
* Add CI/CD pipeline 

This is not covered in the course and this is entirely optional.

If you plan to use this project as your portfolio project, it'll 
definitely help you to stand out from others.

Some links to refer to:

* [Unit Tests + CI for Airflow](https://www.astronomer.io/events/recaps/testing-airflow-to-bulletproof-your-code/)
* [CI/CD for Airflow (with Gitlab & GCP state file)](https://engineering.ripple.com/building-ci-cd-with-airflow-gitlab-and-terraform-in-gcp)
* [CI/CD for Airflow (with GitHub and S3 state file)](https://programmaticponderings.com/2021/12/14/devops-for-dataops-building-a-ci-cd-pipeline-for-apache-airflow-dags/)
* [CD for Terraform](https://towardsdatascience.com/git-actions-terraform-for-data-engineers-scientists-gcp-aws-azure-448dc7c60fcc)
* [Spark + Airflow](https://medium.com/doubtnut/github-actions-airflow-for-automating-your-spark-pipeline-c9dff32686b)