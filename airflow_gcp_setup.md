### Running Airflow with GCP in Docker

### Pre-Reqs

- Make folder in home directory, move gcp-service-accounts-credentials to folder and rename

    cd ~
    mkdir -p ~/.google/credentials/
    mv <path/to/your/service-account-authkeys> ~/.google/credentials/google_credentials.json

- Docker-compose v2.x+ (set the memory minimum 5GB, ideally 8GB). If not enough memory, may lead to airflow-webserver continuously restarting

- Python version: 3.7+

### Airflow Setup

1. Download the official Airflow docker-compose.yml file

   curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

2. In `docker-compose.yml` under `x-airflow-common`:
    * Replace `image` with `build` in order to integrate it with GCP using a Dockerfile

        build:
            context: .
            dockerfile: ./Dockerfile

    * Mount your `google_credentials` in `volumes` section as read-only

        ~/.google/credentials/:/.google/credentials:ro

    * Set environment variables:
        `AIRFLOW__CORE__LOAD_EXAMPLES` = 'false'
        `GCP_PROJECT_ID` = <variable>
        `GCP_GCS_BUCKET` = <variable>
        `GOOGLE_APPLICATION_CREDENTIALS` = <location of google_credentials.json>
        `AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT` = google-cloud-platform://?extra__google_cloud_platform__key_path=<location of google_credentials.json>

3. Make these folders: `dags`, `logs` and `plugins`

    mkdir ./dags ./logs ./plugins

4. On macOS, we need to export environmental variables to ensure that user and group permissions are the same between the folders on host and the containers

    (echo AIRFLOW_UID=$(id -u) & echo AIRFLOW_GID=0) > .env

5. Create a `Dockerfile` using `apache/airflow:2.2.3` as base image
    * Install Google Cloud SDK to connect with GCS bucket (Data Lake)
    * Use `requirements.txt` to install libraries via `pip install`
