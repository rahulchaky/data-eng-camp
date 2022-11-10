import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from to_parquet import format_to_parquet

PROJECT_ID = os.environ.get("GCP_PROJECT_ID" "liquid-terra-367315")
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc_data_lake_liquid-terra-367315")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')

# Environment Variables - These are passed through the .env file.
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
# Location of Google Credentials within Airflow Container
PATH_TO_CREDS = '/.google/credentials/google_credentials.json'

# Download Link that changes for each month AND name and location of output file
# This is the Jinja template for data
URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
URL_TEMPLATE = URL_PREFIX + \
    '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
UNZIP_OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
PARQUET_OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + \
    '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
# Table Template
TABLE_NAME_TEMPLATE = 'yellow_tripdata_{{ execution_date.strftime(\'%Y_%m\') }}'
GCP_PATH_TEMPLATE = 'raw/yellow_tripdata/{{ execution_date.strftime(\'%Y\') }}/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'


# Name of Workflow (Should contain basic information about this workflow)
gcp_yellow = DAG(
    "YellowIngestionDag",
    # refer to the notes on the lab for more information about schedule_interval, start_date is required with schedule interval
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2021, 7, 3),
    max_active_runs=1
)

# Below should define what tasks are going to happen and their dependecies.
with gcp_yellow:

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

    # Third task is to make the csv file a parquet file.
    csv_to_parquet_task = PythonOperator(
        task_id='csv_to_parquet',
        python_callable=format_to_parquet,
        op_kwargs=dict(
            csv_file=UNZIP_OUTPUT_FILE_TEMPLATE
        ),
    )

    # Fourth task is to load the data to GCP
    local_to_gcs_task = BashOperator(
        task_id="local_to_gcs",
        bash_command=f"gcloud auth activate-service-account --key-file={PATH_TO_CREDS} && \
        gsutil -m cp {PARQUET_OUTPUT_FILE_TEMPLATE} gs://{BUCKET}/{GCP_PATH_TEMPLATE}",

    )

    # Fifth task is to delete the data from local storage
    del_data_task = BashOperator(
        task_id="del_data",
        bash_command=f"rm {PARQUET_OUTPUT_FILE_TEMPLATE} {UNZIP_OUTPUT_FILE_TEMPLATE}",
    )

    # Dependencies, basically states what order task have to be completed in
    wget_task >> unzip_task >> csv_to_parquet_task >> local_to_gcs_task >> del_data_task
