# Week 2 Notes
## 2.1.1 Data Lake
### Features of a Data Lake
A **Data Lake** is a central repository that holds BigData from many sources. The idea is to ingest data as quickly as possible and make it available to other team members.
- Ingest structured and unstructured data
- Stores, secures, and protects data at unlimited scale
- Catalogs and indexes for analysis without data movement
- Connects data with analytics and machine learning tools

### Data Lake vs Data Warehouse
Data Lakes and Data Warehouses have 3 key differences: Data, Users, and Use Cases.
- Data Lake
    - Data: Unstructured
    - Users: Data Scientists and Data Analysts
    - Use Cases: Stream Processing, Machine Learning, and Real Time Analysis
- Data Warehouse
    - Data: Structured
    - Users: Business Analysts
    - Use Cases: Batch Processing, BI (Business Intelligence), and Reporting

These difference can be even further expanded
- Data Lakes are:
    - **Raw**: Data Lakes contain unstructured, semi-structured, and structured data with minimal processing. It can be used to contain unconventional data such as log and sensor data.
    - **Large**: Data Lakes contain vast amounts of data in the order of petabytes. Since the data can be in any form or size, large amounts of unstructured data can be stored indefinetely and can be transformed when in use only.
    - **Undefined**: Data in data lakes can be used for a wide variety of applications, such as Machine Learning, Streaming Analytics, and AI.

- Data Warehouses are:
    - **Refined**: Data Warehouses contain highly structured data that is cleaned, pre-processed and refined. This data is stored for very specific use cases such as BI.
    - **Smaller**: Data Warehouses contain less data in the order of terabytes. In order to maintain data cleanliness and health of the warehouse, data must be processed before ingestion and periodic purging of data is necessary.
    - **Relational**: Data Warehouses contain historic and relational data, such as transaction systems, operations, etc.

### Why Data Lakes Exist
- Companies realized the value of data
- Store and access data quickly
- Cannot always define the structure of the data
- Usefulness of data being realized later in the project lifecycle
- Increase in data scientists
- R&D on data products
- Need for cheap storage of BigData

### ETL vs ELT
- **ETL** (Extract Transform and Load) vs **ELT** (Extract Load and Transform)
- **ETL** is mainly used for a small amount of data
- **ELT** is used for a large amount of data
- **ETL** is a Data Warehouse Solution (Schema on Write)
    - Schema on Write: you define a well-defined schema and the relationships and then you write the data.
-  **ELT** is a Data Lake Solution. (Schema on Read)
    - Schema on Read: you write the data first and determine the schema on the read

### Gotcha of Data Lake
Data Swamp: an unmanaged Data Lake that is either inaccessible to intended users or provides little value.\
Reasons a Data Lake can convert into a Data Swamp
- No versioning
- Incompatible schemas for same data without versioning
    - Ex: You are writing trip data as Arrow File Format in one folder and the next day you switch to writing data as Parquet File Format into the same folder. This makes it really hard for consumers to consume this data rendering the dataset useless.
- No metadata associated
    - Generally if you do not associate metadata to your data, it becomes really hard for a person or a data scientist to use your data, to figure out what's the usefulness of your data for the project.
- Joins not possible
    - Generally data lakes also become useless if there is not a possibility to join different data sets. This happens because there is no foreign key available or there is no other possibility to join different data sets.

### Cloud Provider for Data Lake Storage
- GCP: Cloud Storage
- AWS: S3
- Azure: Azure Blobs

## 2.2.1 Workflow Orchestration
### Data Pipeline
A **Data Pipeline** is a script, bunch of scripts, or job that takes in one or more data set(s) and does something to it (via the script/job) and produces one or more data set(s).
- Refer to [ingest_data.py](https://github.com/rahulchaky/data-eng-camp/blob/main/week_1_basics_n_setup/docker_sql/ingest_data.py) from Week 1 for an example of a data pipeline.
    - There exists a csv file on the internet that we want to use.
    - The pipeline first download the file.
    - Then the rest of script puts the data into a Postgres DB.
- There is an issue with this type of data pipeline.
    - This is due to the fact that there are two processes occuring in the same script (downloading and inserting)
        - If either of the two tasks fail (internet dies or connection to DB is lost), the entire script will fail.
        - When dealing with large amounts of data, imagine having to redownload the data everytime the script fails for either reason.
        - We can have a `sleep()` condition for every process that the script is running.
        - Psuedocode Example (attempts dowload process, if fails tries again in 10 seconds):
```
while not_successful():
    os.system(f"wget {url} -O {csv_name}")
    sleep(10)
```
- However, it is ideal to to split each process into its own individual file.
    - Using the above example, the process would like:
    - Online Data -> (Download Script) -> CSV File -> (Ingest Script) -> PostGres DB
        - Basically the online data would be downloading creating a CSV file. This file is then imported to the Postgres Database.
    - Notes: This whole process is still one data pipeline.
- The two scripts both have *params*
    - The download script has the parameter of URL, thus we can take this pipeline and run it for any data that can be download via URL.

Let us take a look at a more complex example:
- Online Data -> (1. Download Script) -> Local CSV File -> (2. Convert CSV to Parquet) -> Local Parquet File -> (3. Upload to Google Cloud) -> Parquet File in Google Cloud -> (4.Upload to BigQuery) -> Table in BigQuery
    - CSV File is not the most effective format to store data so for this week we are using the Parquet file type.
- Notice that there a few *dependencies* in this data pipeline.
    - The 4th step depends on the 3rd step, it already expects that the data is uploaded to Google Cloud.
    - Basically, we need to make sure that everything is executed in the numerical order given.
    - Note: The data pipeline can also have scripts that run in parallel.
        - Ex: Loading the Parquet File to Amazon S3 on top of everything else in the pipeline.

Because of the complexity, we can also call this the **Data Workflow**.
- It specifies how exactly our data flows
- What are the jobs that are executed (each job is noted by a number)
- What are the dependencies that exist (each dependency can be seen by the output of one job being required for the next job)
- Can also be called DAG (Directed Acyclic Graph)
    - Directed (Arrows)
    - Acyclic (There are no cycles, no looping back to a prior step)
- The Data Workflow can also have a global parameter
    - Ex: Month (2021-01), which limits the data to this month
    - On top of this each job would also have its own set of parameters.

Given this workflow, how do we actually execute this?
- How do we make sure the jobs run in order?
- How do we make sure that if a job fails that it can be easily retried so the pipeline does not fail?


Data Workflow Orchestration Tools (for big workflows)
- Examples:
    - Luigi
    - Apache Airflow
    - Prefect
    - Argo
- These tools allow us to specify our data workflows, parameterize them, and run it all.

## Week 2.3.2
Refer to [Airflow Notes](https://github.com/rahulchaky/data-eng-camp/tree/main/week_2_data_ingestion/airflow/docs/1_concepts.md)
Somehow it worked. In airflow direcory:
1. `docker-compose up airflow-init`
2. `docker-compose up`
3. Go to localhost:8080
4. Login u:airflow p:airflow
5. Go to DAG
6. Run it, it will download but fail the unzip.
7. Make new terminal and run `docker ps`
8. `docker exec -it <airflow-scheduler-container-id> bash`
9. List the files and then run `gunzip <data>.csv.gz`
10. Mark the onhold task in DAG as success. This will cause the next task to run.
11. Everything else should work.
The error should be some code logic mistake with how the name is being passed around.