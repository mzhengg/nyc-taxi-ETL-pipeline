1. Build the image (only first-time, or when there's any change in the `Dockerfile`)
    
  docker compose build

2. Initialize the Airflow scheduler, DB, and other configs

  docker compose up airflow-init

3. Run all the services in the docker-compose.yml file:

  docker compose up

4. In another terminal, run `docker compose ps` to see which containers are up & running (there should be 8, matching with the services in your docker-compose file).

5. Login to Airflow web UI on `localhost:8080` with default credentials: `airflow/airflow`

6. Run your DAG on the Web Console

7. On finishing your run or to shut down the container/s:

  docker compose down

  To stop and delete containers, volumes with database data, and download images:

  docker compose down --volumes --rmi all