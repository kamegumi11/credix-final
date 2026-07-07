from datetime import datetime
import subprocess
import sys
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator


PROJECT_ROOT = Path("/opt/airflow/credix")


def run_script(relative_path):
    script_path = PROJECT_ROOT / relative_path

    print(f"Executando script: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
    )

    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Erro ao executar {relative_path}")


with DAG(
    dag_id="credix_credit_pipeline",
    description="Pipeline Credix: Bronze, Silver, Gold, ABT e treinamento do modelo",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["credix", "labfia", "mlops", "credit-risk"],
) as dag:

    data_sanitization = PythonOperator(
        task_id="data_sanitization",
        python_callable=run_script,
        op_args=["datapipeline/data_sanitization.py"],
    )

    application_features = PythonOperator(
        task_id="application_features",
        python_callable=run_script,
        op_args=["datapipeline/application_features.py"],
    )

    bureau_features = PythonOperator(
        task_id="bureau_features",
        python_callable=run_script,
        op_args=["datapipeline/bureau_features.py"],
    )

    generate_abt = PythonOperator(
        task_id="generate_abt",
        python_callable=run_script,
        op_args=["datapipeline/generate_abt.py"],
    )

    train_model = PythonOperator(
        task_id="train_model",
        python_callable=run_script,
        op_args=["model/train.py"],
    )

    data_sanitization >> [application_features, bureau_features] >> generate_abt >> train_model