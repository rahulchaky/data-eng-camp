## Homework for Week 2

The homework can be completed by modifying the files that were created in week 2. However, for my understanding I wanted to start from an empty directory.

Below will just be various status updates and notes on any thoughts, questions, or difficulties I had.

### Setup Phase
- The `docker-compose.yaml` file is directly from Apache Airflow.
- The  `Dockerfile` is the one from the airflow folder.
- The check to see if the GCP credentials was mapped was a success.

### DAG for Yellow Taxi Data
- Imported libraries from other dags.
- Uploading to GCP Cloud Storage was a success.
- Will use web interface to upload to BigQuery.
- I named the file `output_<datetime>`, but I should have used `yellow_taxi_<datetime>` as it would have provided better clarity.
- Running this process takes a really long time so I will manually change the name in GCP.
- I ended up rerunning the whole process as there were various errors and I also wanted to have the tables neatly stored via a file path.

### DAG for FHV Data
- Copied over files from Yellow Taxi Data and edited them 


### DAG for Taxi Zones Data
- Copied over files from Yellow Taxi Data and edited them 

### Cleanup
- I consolidated all the DAGs into the same folder as there was no need to have them in separate folders. All of the necessary files were successfully added to GCP Cloud Storage.

### Uploading the Data to BigQuery
1. Go to BigQuery.

2. Click on the three dots next to your project and click on 'Create Dataset'.

3.  Give the dataset an ID and set the location as the same as the files in the cloud storage. Then click on 'Create Dataset'.

4. Now run this query for each table that you want to create:
```
CREATE OR REPLACE EXTERNAL TABLE liquid-terra-367315.nytaxi.<table_name>
OPTIONS (
    format = 'parquet',
    uris = [
        'gs://dtc_data_lake_liquid-terra-367315/raw/yellow_tripdata/2019/*',
        'gs://dtc_data_lake_liquid-terra-367315/raw/yellow_tripdata/2020/*'
    ]
)
```

5. Now you should see the tables in BigQuery.