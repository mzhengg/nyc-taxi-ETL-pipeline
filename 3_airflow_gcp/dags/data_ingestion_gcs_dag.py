import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from google.cloud import bigquery

# TODO: use the same value as `bq_dataset_id` in variables.tf
bq_dataset_id = "trips_data_all"

# retrieve environmental variables from local environment (Dockerfile image)
gcp_project_id = os.environ.get("GCP_PROJECT_ID", None)
gcp_gcs_bucket = os.environ.get("GCP_GCS_BUCKET", None)
path_to_local_home = os.environ.get("AIRFLOW_HOME", None)

# download dataset
parquet_file = "yellow_tripdata_2021-01.parquet"
parquet_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{parquet_file}"

# bigquery table name
table_name = parquet_file.split('.')[0]

def upload_to_gcs(bucket_name, blob_name, local_file):
    # in gcs, you store blob objects (data) in bucket objects (containers)

    # client to bundle configuration needed for API requests
    client = storage.Client()

    # factory constructor for bucket object
    bucket = client.bucket(bucket_name)

    # factory constructor for blob object
    blob = bucket.blob(blob_name)

    # upload this blob's contents from the content of a named file
    blob.upload_from_filename(local_file)

# ref: https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet
def gcs_to_bigquery(gcp_gcs_bucket, gcs_file, project_id, dataset_id, table_name):
    # in bigquery, tables are stored as project_id > dataset_id > table_id
    table_id = f'{project_id}.{dataset_id}.{table_name}'

    # client to bundle configuration needed for API requests
    client = bigquery.Client()

    # specifying file format (csv, parquet, etc.)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
    )
    # location of file in gcs
    uri = f"gs://{gcp_gcs_bucket}/raw/{gcs_file}"

    # make an API request to upload data
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

default_args = {
    "owner": "airflow",
    "start_date": '2022-1-1',
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=['dtc-de'],

) as dag:
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {parquet_url} > {path_to_local_home}/{parquet_file}"
    )

    upload_to_gcs_task = PythonOperator(
        task_id="upload_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": gcp_gcs_bucket,
            "blob_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}"
        }
    )

    gcs_to_bigquery_task = PythonOperator(
        task_id="gcs_to_bigquery_task",
        python_callable=gcs_to_bigquery,
        op_kwargs={
            "gcp_gcs_bucket": gcp_gcs_bucket,
            "gcs_file": parquet_file,
            "project_id": gcp_project_id,
            "dataset_id": bq_dataset_id,
            "table_name": table_name
        }
    )

    download_dataset_task >> upload_to_gcs_task >> gcs_to_bigquery_task