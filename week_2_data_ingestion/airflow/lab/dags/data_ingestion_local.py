import os
from datetime import datetime

# Creating a DAG (workflow) to run via Airflow
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Importing the function from the ingest script
from ingest_script import ingest_callable

# Environment Variables - These are passed through the .env file.
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# Postgres Environment Variables
PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

# Download Link that changes for each month AND name and location of output file
# This is the Jinja template for data
URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
URL_TEMPLATE = URL_PREFIX + \
    '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
# Table Template
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'


# Name of Workflow (Should contain basic information about this workflow)
local_workflow = DAG(
    "LocalIngestionDag",
    # refer to the notes on the lab for more information about schedule_interval, start_date is required with schedule interval
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1)
)

# Below should define what tasks are going to happen and their dependecies.
with local_workflow:

    # First task is to get the data
    # The reason we use curl is because wget is not installed with airflow
    # '-sS' is required, the 'L' is so that if the link redirects somewhere first then it will follow.
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
    )

    # Second task is to unzip the .csv.gx files. Should return a .csv file.
    unzip_task = BashOperator(
        task_id='unzip',
        bash_command=f'gunzip {OUTPUT_FILE_TEMPLATE}'
    )

    # Third task is to ingest the data to Postgres
    ingest_task = PythonOperator(
        task_id='ingest',
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME_TEMPLATE,
            csv_file=OUTPUT_FILE_TEMPLATE
        ),
    )

    # Dependencies, basically states what order task have to be completed in
    wget_task >> unzip_task >> ingest_task
