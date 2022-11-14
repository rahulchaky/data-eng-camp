# Analytics Engineering Notes

## Dealing with Prerequistes
**Ingesting the Green Taxi Data - Years 2019 and 2020**\
I made a [file](https://github.com/rahulchaky/data-eng-camp/blob/main/week_2_data_ingestion/airflow/hw/dags/green_taxi_dag.py) to ingest the Green Taxi data. This process was slightly different as the backup csv links did not work. I ended up using the parquet files provided directly from the [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Then, I created a table in BigQuery using the files that were uploaded to GCS.
```
CREATE OR REPLACE EXTERNAL TABLE liquid-terra-367315.nytaxi.green_tripdata
OPTIONS (
    format = 'parquet',
    uris = [
        'gs://dtc_data_lake_liquid-terra-367315/raw/green_tripdata/2019/*',
        'gs://dtc_data_lake_liquid-terra-367315/raw/green_tripdata/2020/*'
    ]
)
```

## Setting up dbt for using BigQuery
- [Instructions](https://github.com/rahulchaky/data-eng-camp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
- I had no issues in setting up dbt.

