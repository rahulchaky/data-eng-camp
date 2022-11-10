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