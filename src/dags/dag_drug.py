import os
from datetime import datetime
from airflow import DAG
from airflow.sensors.filesystem import FileSensor

import constant
from operator_drug import (
    CopyFileOperator,
    DrugsSilverOperator,
    ClinicalTrialsSilverOperator,
    PubmedMergeOperator,
    PubmedSilverOperator,
    DrugGraphGoldOperator,
)


with DAG(
    dag_id="drug",
    start_date=datetime(2023, 11, 28),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    drugs_sensor = FileSensor(
        task_id="drugs_sensor",
        filepath=os.path.join(constant.DAGS_FOLDER, constant.EXTERNAL_DRUGS_FILE),
        poke_interval=constant.EXTERNAL_FILE_SENSOR_POKE_INTERVAL,
        timeout=constant.EXTERNAL_FILE_SENSOR_POKE_TIMEOUT,
    )

    drugs_bronze = CopyFileOperator(
        task_id="drugs_bronze",
        source_folder=constant.DAGS_FOLDER,
        source_path=constant.EXTERNAL_DRUGS_FILE,
        destination_folder=constant.DAGS_FOLDER,
        destination_path=constant.BRONZE_DRUGS_FILE,
    )

    drugs_silver = DrugsSilverOperator(
        task_id="drugs_silver",
        source_file=constant.BRONZE_DRUGS_FILE,
        destination_file=constant.SILVER_DRUGS_FILE,
    )

    clinical_trials_sensor = FileSensor(
        task_id="clinical_trials_sensor",
        filepath=os.path.join(
            constant.DAGS_FOLDER, constant.EXTERNAL_CLINICAL_TRIALS_FILE
        ),
        poke_interval=constant.EXTERNAL_FILE_SENSOR_POKE_INTERVAL,
        timeout=constant.EXTERNAL_FILE_SENSOR_POKE_TIMEOUT,
    )

    clinical_trials_bronze = CopyFileOperator(
        task_id="clinical_trials_bronze",
        source_folder=constant.DAGS_FOLDER,
        source_path=constant.EXTERNAL_CLINICAL_TRIALS_FILE,
        destination_folder=constant.DAGS_FOLDER,
        destination_path=constant.BRONZE_CLINICAL_TRIALS_FILE,
    )

    clinical_trials_silver = ClinicalTrialsSilverOperator(
        task_id="clinical_trials_silver",
        source_file=constant.BRONZE_CLINICAL_TRIALS_FILE,
        destination_file=constant.SILVER_CLINICAL_TRIALS_FILE,
    )

    pubmed_a_sensor = FileSensor(
        task_id="pubmed_a_sensor",
        filepath=os.path.join(constant.DAGS_FOLDER, constant.EXTERNAL_PUBMED_A_FILE),
        poke_interval=constant.EXTERNAL_FILE_SENSOR_POKE_INTERVAL,
        timeout=constant.EXTERNAL_FILE_SENSOR_POKE_TIMEOUT,
    )

    pubmed_a_bronze = CopyFileOperator(
        task_id="pubmed_a_bronze",
        source_folder=constant.DAGS_FOLDER,
        source_path=constant.EXTERNAL_PUBMED_A_FILE,
        destination_folder=constant.DAGS_FOLDER,
        destination_path=constant.BRONZE_PUBMED_A_FILE,
    )

    pubmed_b_sensor = FileSensor(
        task_id="pubmed_b_sensor",
        filepath=os.path.join(constant.DAGS_FOLDER, constant.EXTERNAL_PUBMED_B_FILE),
        poke_interval=constant.EXTERNAL_FILE_SENSOR_POKE_INTERVAL,
        timeout=constant.EXTERNAL_FILE_SENSOR_POKE_TIMEOUT,
    )

    pubmed_b_bronze = CopyFileOperator(
        task_id="pubmed_b_bronze",
        source_folder=constant.DAGS_FOLDER,
        source_path=constant.EXTERNAL_PUBMED_B_FILE,
        destination_folder=constant.DAGS_FOLDER,
        destination_path=constant.BRONZE_PUBMED_B_FILE,
    )

    pubmed_merge_silver = PubmedMergeOperator(
        task_id="pubmed_merge_silver",
        source_files=[constant.BRONZE_PUBMED_A_FILE, constant.BRONZE_PUBMED_B_FILE],
        destination_file=constant.SILVER_PUBMED_MERGED_FILE,
    )

    pubmed_silver = PubmedSilverOperator(
        task_id="pubmed_silver",
        source_file=constant.SILVER_PUBMED_MERGED_FILE,
        destination_file=constant.SILVER_PUBMED_FILE,
    )

    drug_graph_gold = DrugGraphGoldOperator(
        task_id="drug_graph_gold",
    )


drugs_sensor >> drugs_bronze >> drugs_silver >> drug_graph_gold
(
    clinical_trials_sensor
    >> clinical_trials_bronze
    >> clinical_trials_silver
    >> drug_graph_gold
)
pubmed_a_sensor >> pubmed_a_bronze >> pubmed_silver >> drug_graph_gold
pubmed_b_sensor >> pubmed_b_bronze >> pubmed_silver >> drug_graph_gold


if __name__ == "__main__":
    dag.test()
