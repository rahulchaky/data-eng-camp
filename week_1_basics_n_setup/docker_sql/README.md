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

## Dataset Location
https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

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
Create a network
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
