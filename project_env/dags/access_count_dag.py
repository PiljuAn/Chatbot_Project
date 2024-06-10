from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pytz

from pipeline.extract import extractor
from pipeline.load import loader

from db.connector import DBconnector
from db import queries
from utils.setting import DB_SETTINGS
from utils.execution_time_check import ElapseTime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 3, 8, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'codegenius_access_count',
    default_args=default_args,
    schedule_interval='@daily'
)

#####################
### etl pipe line ###
#####################

def extract_data(**kwargs):
    db_obj = DBconnector(**DB_SETTINGS["DJANGO_db"])
    table_name = "codegenius_access_count"
    _date = datetime.now() - timedelta(days=1)
    batch_date = _date.date()
    with ElapseTime():
        print("extract_data 시작")
        extracted_data = extractor(db_connector=db_obj, table_name=table_name, batch_date=batch_date)
        kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)

def load_to_pg(**kwargs):
    db_obj = DBconnector(**DB_SETTINGS["DJANGO_datamart"])
    table_name = "access_count"
    ti = kwargs['ti']
    processed_df = ti.xcom_pull(key='extracted_data', task_ids='Extract_Log')
    print(processed_df)
    with ElapseTime():
        print("load_to_pg 시작")
        loader(df=processed_df, db_connector=db_obj, table_name=table_name)

############
### task ###
############

with dag:
    extract_data_task = PythonOperator(
        task_id='Extract_Log',
        python_callable=extract_data,
        provide_context=True
    )
    load_to_pg_task = PythonOperator(
        task_id='Load_to_postgresql',
        python_callable=load_to_pg,
        provide_context=True
    )

#######################
### task dependency ###   
#######################

extract_data_task >> load_to_pg_task