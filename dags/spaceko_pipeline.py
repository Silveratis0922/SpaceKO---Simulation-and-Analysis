from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, "/opt/airflow")

def run_simulation():
    sys.path.insert(0, "/opt/airflow/simulation_V2")
    from main import main as simulation_main
    simulation_main()

def run_bronze():
    from pipeline.bronze.upload_bronze import upload_to_bronze
    upload_to_bronze()

def run_silver():
    from pipeline.silver.transform_silver import main as silver_main
    silver_main()

def run_load_postgres():
    from pipeline.gold.load_postgres import main as postgres_main
    postgres_main()

def run_gold():
    load_dotenv("/opt/airflow/.env")
    engine = create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}"
    )
    sql = open("/opt/airflow/dags/gold_results.sql").read()
    sql = sql.replace("{{source('public', 'silver_results')}}", "public.silver_results")
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS gold.gold_results CASCADE"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))
        conn.execute(text(f"CREATE OR REPLACE VIEW gold.gold_results as {sql}"))
    print("Gold view created !")

with DAG(
    dag_id="spaceko_pipeline",
    start_date=datetime(2026,1,1),
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="simulation",
        python_callable=run_simulation,
    )

    t2 = PythonOperator(
        task_id="bronze",
        python_callable=run_bronze,
    )

    t3 = PythonOperator(
        task_id="silver",
        python_callable=run_silver,
    )

    t4 = PythonOperator(
        task_id="load_postgres",
        python_callable=run_load_postgres,
    )

    t5 = PythonOperator(
        task_id="gold",
        python_callable=run_gold,
    )

    t1 >> t2 >> t3 >> t4 >> t5