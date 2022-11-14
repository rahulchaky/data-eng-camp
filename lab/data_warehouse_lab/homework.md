## Homework

### Question 1: 
**What is count for fhv vehicles data for year 2019**  
Can load the data for cloud storage and run a count(*)

Solution:
1. Loading the fhv_2019 data from Google Cloud Storage into an external table
The pseudocode is found below.[^1]
```
CREATE OR REPLACE EXTERNAL TABLE liquid-terra-367315.nytaxi.<table_name>
OPTIONS (
    format = 'parquet',
    uris = [
        'gs://dtc_data_lake_liquid-terra-367315/raw/yellow_tripdata/2019/*',
        'gs://dtc_data_lake_liquid-terra-367315/raw/yellow_tripdata/2020/*'
    ]
);
```

[^1]:We have done this in the week 2 homework.

2. Finding the count
```
SELECT COUNT(*) FROM `liquid-terra-367315.nytaxi.fhv_tripdata`;
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

Solution:\
**Answer: Partition by dropoff_datetime and cluster by dispatching_base_num**\
We know that `dropoff_datetime` contains data of the type Timestamp. This means we can partition using this column. On the other hand, `dispatching_base_num` contains data of type String. We cannot partition on this type, therefore we need to cluster by this type. 

### Question 4: 
**What is the count, estimated and actual data processed for query which counts trip between 2019/01/01 and 2019/03/31 for dispatching_base_num B00987, B02060, B02279**  
Create a table with optimized clustering and partitioning, and run a 
count(*). Estimated data processed can be found in top right corner and
actual data processed can be found after the query is executed.

Solution:
1. Creating a table with clustering and partitioning
```
CREATE OR REPLACE TABLE `liquid-terra-367315.nytaxi.fhv_tripdata_partitioned`
PARTITION BY DATE(dropoff_datetime)
CLUSTER BY dispatching_base_num AS (
    SELECT * FROM `liquid-terra-367315.nytaxi.fhv_tripdata`
);
```
The created table is what was described from the previous question. This question is asking to "filter by `dropoff_datetime` and filter by `dispatching_base_num`".

2. Counting trips
```
SELECT COUNT(*) FROM `liquid-terra-367315.nytaxi.fhv_tripdata_partitioned`
WHERE dropoff_datetime BETWEEN '2019-01-01' AND '2019-03-31'
AND dispatching_base_num IN ('B00987', 'B02060', 'B02279');
```
Note: The partitioned table is processing about 200MB less data than if we were using the unpartitioned table.
- Unpartitioned Estimate: ~600MB
- Partitioned Estimate: ~400MB
- Actual Data Use: 136MB
- Count: 26558

The reason that there is a difference between the Partitioned Estimate and the Actual Data Use is because the table is clustered. Remember that when a table is clustered the data that is processed faster due to clustering cannot be calculated by BigQuery.

**Answer: Count: 26658, Estimate: ~400MB, Actual Data Use: 136MB**

### Question 5: 
**What will be the best partitioning or clustering strategy when filtering on dispatching_base_num and SR_Flag**  
Review partitioning and clustering video. 
Partitioning cannot be created on all data types.

Solution:\
Remeber for this type of question, we need to look at the type of data found in each column.
- `dispatching_bas_num`: String
- `SR_Flag`: Integer

The given answer is to cluster by both, however with a bit of querying you can see that `SR_Flag` is actually a range of integers from 1 to 42. Therefore, in this case we should partition by `SR_Flag` and cluster by `dispatching_num_base`.

**Answer: Partition by `SR_Flag` and Cluster by `dispatching_num_base`**

### Question 6: 
**What improvements can be seen by partitioning and clustering for data size less than 1 GB**  
Partitioning and clustering also creates extra metadata.  
Before query execution this metadata needs to be processed.

Solution:

**Answer: No improvements and can be worse due to metadata**

### Question 7: 
**In which format does BigQuery save data**  
Review big query internals video.

Solution:

<<<<<<< Updated upstream
**Answer: **
=======
**Answer: Columnar**
>>>>>>> Stashed changes
