## Homework 1
### Q1
Google Cloud SDK 407.0.0

### Q2
Success

### Q3
```
SELECT COUNT(*) FROM yellow_taxi_trips t
WHERE CAST(t."tpep_pickup_datetime" AS DATE) = '2021-01-15';
```
Ans: 53024

### Q4
```
SELECT date_trunc('day', tpep_pickup_datetime) AS pickup_day, MAX(tip_amount) AS max_tip
FROM yellow_taxi_trips t
GROUP BY 1
ORDER BY max_tip DESC
LIMIT 1;
```
Ans: $1140.44

### Q5
```
SELECT date_trunc('day', tpep_pickup_datetime) AS pickup_day, MAX(tip_amount) AS max_tip
FROM yellow_taxi_trips t
GROUP BY 1
ORDER BY max_tip DESC
LIMIT 1;
```
Ans: Upper East Side South (97)

### Q6
```
SELECT CONCAT(COALESCE(puz."Zone", 'Unknown'),
			  ' / ',
			  COALESCE(doz."Zone", 'Unknown')) AS z2z,
AVG(total_amount) AS avg_cost
FROM yellow_taxi_trips t
LEFT JOIN zones puz ON t."PULocationID" = puz."LocationID"
LEFT JOIN zones doz ON t."DOLocationID" = doz."LocationID"
GROUP BY 1
ORDER BY avg_cost DESC
LIMIT 1;
```
Ans: Alphabet City / Unknown ($2292.40)