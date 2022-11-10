## Lab Folder

This folder contains the files and setup for the goal of ingesting data to local Postgres Database using Airflow.
- [Walkthrough](https://www.youtube.com/watch?v=s2U8MWJH5xA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)

This was made to get a better understanding of the entire process. It also is so that the main airflow folder won't be as cluttered.

The finished files were already in the dags_local folder, but I wanted to do the entire process myself as well. Ideally this will solve any confusion that I had as seen in the [Week 2.3.2](https://github.com/rahulchaky/data-eng-camp/blob/main/week_2_data_ingestion/notes.md) notes.

- [Link to Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)

### Notes

The goal of the notes is to detail the process of ingesting data to local Postgres Database using Airflow.\
Note: A lot of these steps are the same as the ones found in the [setup](https://github.com/rahulchaky/data-eng-camp/blob/main/week_2_data_ingestion/airflow/1_setup_official.md) file.

1. The first step was to copy the docker-compose.yaml file from the airflow folder. This file is the official docker file for running airflow. For this exercise, I will suppose that lab is the top level directory when running things.

2. Create dags, logs, and plugins folders. The docker-compose.yaml file looks for `./dags` folder to find the python scripts that make up the pipeline. For this step I ran:
    - `mkdir -p ./dags ./logs ./plugins`

3. Create .env file and add Airflow UID. I am not sure the exact reason this is needed however. This can be done by running:
    - `echo -e "AIRFLOW_UID=$(id -u)" > .env`

4. Now you need the Dockerfile and requirements.txt. I copied the ones from prior. The details about these files can be found in the setup guide that was linked above.
    - I commented out the GCP connection part because it is not needed for this lab. This also speeds up step 6.

5. You also need the scripts folder with the `entrypoint.sh` file from earlier to connect with Airflow.

6. Run `docker-compose build`. This might take some time.

7. Run `docker-compose up`.

8. Since the port is set to 8080 in the `docker-compose.yaml` file. We can access the airflow UI by going to localhost:8080 in a web broswer.

9. In this case, the username and password are both airflow. After logging in, you see that there are no DAGs in airflow as we have yet to create one.

10. Create a DAG. The DAG linked below has comments throughout the code to help understand what the code is doing.
    - [data_ingestion_local.py](https://github.com/rahulchaky/data-eng-camp/blob/main/week_2_data_ingestion/airflow/lab/dags/data_ingestion_local.py)
    - `schedule_interval` allows you to set up how often you want to run the DAG, such as running it once, monthly, yearly, etc.
        - [Documentation on Schedule Interval](https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html)
        - [Cron Expression](https://crontab.guru/)
        - In the python file, we have: `schedule_interval="0 6 2 * *"`
            - Using the above resources we can see that this means the job will execute at 6AM on the 2nd day of every month.

11. Now in the Airflow UI, you should see a DAG named `LocalIngestionDag`.
![DAG](airflowdag.PNG)
- Troubleshooting:
    - Make sure the syntax is correct.
    - Try restarting the whole setup.
        - Exit the running process (Ctrl+C)
        - `docker-compose down`
        - `docker-compose build`
        - `docker-compose up airflow-init`
        - `docker-compose up`
        - Go to localhost:8080 and see if it works again.

12. Click on the DAG. Here you can see the DAG tree. The graph tab depicts a more clear version. Now try to run the DAG file.
    - Currently at this step the tasks were not fully implemented. Instead there was some filler to test if it works. Currently both tasks use the BashOperator.
    - The first task is supposed to print Hello World (`echo "Hello World"`) and the second task is supposed to print the parent working directory (`pwd`).

13. When you run the DAG file the airflow scheduler will trigger and if you refresh the page, or turn on autorefresh you can see that all of the tasks complete. If you check the logs of each of the tasks you will see that the expected outputs match what we said each task was supposed to print. Also note the start date of the DAG and for what time each task was executed. This aligns with the `schedule_interval` that was mentioned earlier.

14. Now we go back and edit the DAG so that the first task downloads the files and stores them. The second task in this situation just prints the directory where we expect the downloaded files to be.
    - In the first task, instead of using wget instead we used curl. This is because wget was not installed in the docker container with airflow.
    - If you want to use wget you can add a `RUN` argument to the Dockerfile to download wget.

15. Now run the DAG again. This can be done by clicking on DAG node and clicking clear.

16. To check that the files are where we expected them we can use these steps:
    - `docker ps`
    - Find the `airflow-scheduler` container ID.
    - `docker exec -it <airflow-scheduler_container_ID> bash`
    - This allows us to run linux commands in the `AIRFLOW_HOME` location.
    - List the files
    - You should see the .csv.gz files here.
    - We can add a third task to unzip the files here as well.

17. Reset the environment:
    - First go back to airflow homepage.
    - Then click on the green circle with a number that indicated number of runs.
    - Select all the runs and delete them.
    - This will empty out the dag.
    - In `AIRFLOW_HOME`, delete the .csv.gz files.

18. Add the third task. This task is called `unzip`.

19. Reload the Airflow UI and notice that the DAG has updated.

20. Run the DAG and check if everything went as expected.
    - If everything went well, you should have a bunch of csv files that are organized by month.
    - You may notice that there are a bunch of failed tasks. This is because if you look at the link for the data provided above the data spans only until 2021-07. Considering that the start date that we are using 2021-01, we should have 7 .csv files.

21. Now we need to take the data from the temp folder that airflow created and move it into the Postgres Database.

22. First create a new python file in the dags folder. This file will contain the script to move the data to Postgres. In this case, I used the file from week 1 as it has an identical function.

23. This file has dependencies of pandas, sqlalchemy, and psycopg2; none of which we have installed in the airflow container. To fix this we need to add a line to the dockerfile and reboot everything. We can add:
    - `RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary`

24. Now run `docker-compose build`. This has now added the necessary libraries to the container.

25. Now we need to add the way to connect Postgres to the script. We can do this by adding the Postgres Variables the function engine needs to connect to into the .env file. These variables can be found by looking at what docker needed to connect to Postgres from week 1. We also need to add them to the `docker-compose.yaml` file.

26. Now we need to know how to combine the `docker-compose.yaml` file that we have here with the same file from week 1, as that file is how we connect to Postgres.

27. First, run `docker ps` and make sure no containers are running. After that run `docker-compose up` to start Airflow up.

28. In a new terminal run `docker network ls` and find the relevant network. In the future, this is not necessary. The network will always be `<folder_name>_default`.
    - In this case, since everything is in the `lab` directory, the network is called `lab_default`.

29. Now we need to connect the `docker-compose.yaml` file from here with the one in week 1. For the sake of having everything in one place, I copied the `docker-compose.yaml` file from week 1 into its own directory. The idea is that we will have two separate containers, one for airflow and the other for postgres, but they will be in the same network.

30. Once the `docker-compose.yaml` file has been copied into its own directory, we can add the network. The code block below is what worked for me. Now run this docker-compose file.
    - I often got errors regarding the external network.
    - [Stack Overflow Possible Solutions](https://stackoverflow.com/questions/38088279/communication-between-multiple-docker-compose-projects)
```
networks:
    lab_default:
        external: true
```

31. Run `pgcli -h localhost -p 5432 -U root -d ny_taxi` to test if Postgres is running.

32. Now we need to test if Postgres is connected to the Airflow container.
    - Run `docker ps` and open `bash` of `airflow-scheduler`.
    - Run `python`
    - Run `from sqlalchemy import create_engine`
    - Run `engine = create_engine('postgresql://root:root@pgdatabase:5432/ny_taxi')`
        - This is intended to be `(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')`
    - Then finally, `engine.connect()`.
    - If successful it should print something like this:
        - `<sqlalchemy.engine.base.Connection object at 0x7fe110dc0ed0>`

33. Now we need to check if the DAG functions properly following all the changes made to the Python scripts.
    - Note: Airflow Tasks are **idempotent**.
        - This means that if some task were run over and over again it would produce the same reults. Basically it doesn't matter if:
            - the task breaks halfway and then successfully finishes 
            - the task is run once
            - the the task is run multiple times
        - All of these cases should present the same output.
        - This is why we keep the line:
            - `df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')`

34. Clear the DAG and start up the relevant tasks (the first 7) as only the csv files for those exist.

35. If finished successfully, you can check if the tables have shown up in Postgres using `pgcli`.

36. This is a lot more complicated since you don't have to really mess with setting up a network to transfer to local database. However, if you have reached this point the original goal has been achieved!