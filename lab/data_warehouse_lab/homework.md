## Homework

### Question 1: 
**What is count for fhv vehicles data for year 2019**  
Can load the data for cloud storage and run a count(*)

Solution:
1. Loading the fhv_2019 data from Google Cloud Storage into an external table
The pseudocode is found below.\
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

We have done this in the week 2 homework.

2. Finding the count
```
SELECT COUNT(*) FROM `liquid-terra-367315.nytaxi.fhv_tripdata`
```
**Answer: 42,084,899**

### Question 2: 
**How many distinct dispatching_base_num we have in fhv for 2019**  
Can run a distinct query on the table from question 1

Solution:
```
SELECT COUNT(DISTINCT(dispatching_base_num)) FROM `liquid-terra-367315.nytaxi.fhv_tripdata`;
```
**Answer: 792**

### Question 3: 
**Best strategy to optimise if query always filter by dropoff_datetime and order by dispatching_base_num**  
Review partitioning and clustering video.   
We need to think what will be the most optimal strategy to improve query 
performance and reduce cost.

Solution:

**Answer: **

### Question 4: 
**What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279**  
Create a table with optimized clustering and partitioning, and run a 
count(*). Estimated data processed can be found in top right corner and
actual data processed can be found after the query is executed.

Solution:

**Answer: **

### Question 5: 
**What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag**  
Review partitioning and clustering video. 
Partitioning cannot be created on all data types.

Solution:

**Answer: **

### Question 6: 
**What improvements can be seen by partitioning and clustering for data size less than 1 GB**  
Partitioning and clustering also creates extra metadata.  
Before query execution this metadata needs to be processed.

Solution:

**Answer: **

### Question 7: 
**In which format does BigQuery save data**  
Review big query internals video.

Solution:

**Answer: **