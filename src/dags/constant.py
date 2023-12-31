import os

from airflow.configuration import conf


DAGS_FOLDER = conf.get("core", "dags_folder")

EXTERNAL_FOLDER = os.path.join(DAGS_FOLDER, "data", "external")
EXTERNAL_DRUGS_FILE = os.path.join(EXTERNAL_FOLDER, "drugs.csv")
EXTERNAL_CLINICAL_TRIALS_FILE = os.path.join(EXTERNAL_FOLDER, "clinical_trials.csv")
EXTERNAL_PUBMED_A_FILE = os.path.join(EXTERNAL_FOLDER, "pubmed.csv")
EXTERNAL_PUBMED_B_FILE = os.path.join(EXTERNAL_FOLDER, "pubmed.json")

BRONZE_FOLDER = os.path.join(DAGS_FOLDER, "data", "bronze")
BRONZE_DRUGS_FILE = os.path.join(BRONZE_FOLDER, "drugs.csv")
BRONZE_CLINICAL_TRIALS_FILE = os.path.join(BRONZE_FOLDER, "clinical_trials.csv")
BRONZE_PUBMED_A_FILE = os.path.join(BRONZE_FOLDER, "pubmed.csv")
BRONZE_PUBMED_B_FILE = os.path.join(BRONZE_FOLDER, "pubmed.json")

SILVER_FOLDER = os.path.join(DAGS_FOLDER, "data", "silver")
SILVER_DRUGS_FILE = os.path.join(SILVER_FOLDER, "drugs.json")
SILVER_CLINICAL_TRIALS_FILE = os.path.join(SILVER_FOLDER, "clinical_trials.json")
SILVER_PUBMED_MERGED_FILE = os.path.join(SILVER_FOLDER, "pubmed_merged.json")
SILVER_PUBMED_FILE = os.path.join(SILVER_FOLDER, "pubmed.json")

GOLD_FOLDER = os.path.join(DAGS_FOLDER, "data", "gold")
DRUG_GRAPH_FILE = os.path.join(GOLD_FOLDER, "drug_graph.json")
TOP_QUOTER_FILE = os.path.join(GOLD_FOLDER, "top_quoter.json")
EXCLUSIVE_DRUG_SET_FILE = os.path.join(GOLD_FOLDER, "exclusive_drug_set.json")
