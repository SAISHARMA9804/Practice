from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime

# Define DAG arguments
default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Create the DAG
with DAG(
    dag_id='gcs_to_bq_transformation',
    default_args=default_args,
    schedule_interval=None,  # Or a cron schedule, e.g., '0 0 * * *' for daily at midnight
    catchup=False,
) as dag:
    # Task to load data from GCS to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq',
        bucket='your-gcs-bucket',  # Replace with your GCS bucket name
        source_objects=['your-data-file.csv'],  # Replace with your GCS file path
        destination_project_dataset_table='your-project.your_dataset.your_table',  # Replace with your BigQuery table
        source_format='CSV',  # Or 'JSON', 'AVRO', 'PARQUET'
        skip_leading_rows=1,  # If your CSV has a header row
        write_disposition='WRITE_TRUNCATE',  # Or 'WRITE_APPEND', 'WRITE_EMPTY'
        schema_fields=[  # Define your BigQuery schema
            {'name': 'column1', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'column2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            # Add more columns as needed
        ],
    )