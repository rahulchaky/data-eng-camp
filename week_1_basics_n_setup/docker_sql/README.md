# Week 1 Notes

## Running PG in Docker
```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/ronch/Desktop/Code/Git/data-eng-camp/week_1_basics_n_setup/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

## Access PGCLI
```
pgcli -p 5432 -u root -d ny_taxi
```

## NY Trips Dataset
- This provides information about what each column means
  - https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- URL for the data for this week
  - https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

## PGAdmin in Docker
Open localhost:8080 in browser
```
docker run -it \ 
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \ 
  -p 8080:80 \
  dpage/pgadmin4
```

## Network
### Create a network
```
docker network create pg-network
```

### Connects to set network
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin \
  dpage/pgadmin4
```

### Connects PG to the created network (can access via name and given port)
```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/ronch/Desktop/Code/Git/data-eng-camp/week_1_basics_n_setup/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

**Quick Note Regarding Docker**\
Using Docker Desktop, you can choose to when the containers are running or not. This way you only have to run all of the docker commands once.

## 1.2.4 Notes[^1]
### Converting Jupyter Notebook into Python Script
This file was renamed to ingest_data.py
```
jupyter nbconvert --to=script upload-data.ipynb
```

### Running ingest_data.py
This creates a .gz file in the directory, however since the file is not >100MB it can be pushed to github.
```
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

### Creating a Docker container again
This is a docker container that runs ingest_data.
```
docker build -t taxi_ingest:v001 .
```
Running the script with Docker:
The first tab in is parameters to 'docker', the second are parameters to 'taxi_ingest:v001'.
In real life, the host would be a url that links to the database. Generally this entire step would not be done via docker but through something like Kubernetes.
```
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```
[^1]: I didn't really start taking notes until here. However, there are various edits made above to make things a little clearer.

# 1.2.5 Notes
Goal of 1.2.5 is to have one '.yaml' file to have everything set up in. Basically we need some file that creates two containers, one Postgres and one PGAdmin, and a network that the two of them belong to.

To this we will use **Docker Compose**. If you have Docker Desktop, this is already installed with Docker.
Running Docker-Compose:
```
docker-compose up
```
Unfortunately once we login to localhost:8080, we have to add the server again.
1. Login via PGAdmin username and password.
2. Click on Add New Server.
3. Give the server a name.
4. Click on the connection tab.
5. Since we are connecting to the other container, the name is the other container's name (in this case it is pgdatabase).
6. Enter the username and password from postgres.
7. Save and you should be connected.

Closing Containers and Docker-Compose
1. Go to the terminal where you ran docker-compose.
2. Press Ctrl+C. This stops running the docker containers.
3. Shut the docker-compose down.
Shutting Down Docker-Compose:
```
docker-compose down
```
This deletes the containers from memory.

If you run:
```
docker-compose up -d
```
You get the terminal back, meaning there isnt a scrolling wall of text desribing the processes running. This is convenient, although you could always use multiple terminal windows. To shut it down in this case, we can run the same command to shut down docker compose and it will stop running the containers and delete them.