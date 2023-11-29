import os
import re
import shutil
from typing import Any, List, Dict
from collections import defaultdict
import json
import json5
import pandas as pd
import utils
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context


class CopyFileOperator(BaseOperator):
    # The API of this operator has been designed to look like GCSToGCSOperator.
    # This will ease the rewrite because we will realistically not process local files in production.
    def __init__(
        self,
        source_folder: str,
        source_path: str,
        destination_folder: str,
        destination_path: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_folder = source_folder
        self.source_path = source_path
        self.destination_folder = destination_folder
        self.destination_path = destination_path

    def execute(self, context: Context) -> Any:
        shutil.copyfile(
            os.path.join(self.source_folder, self.source_path),
            os.path.join(self.destination_folder, self.destination_path),
        )


class DrugsSilverOperator(BaseOperator):
    def __init__(
        self,
        source_file: str,
        destination_file: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_file = source_file
        self.destination_file = destination_file

    def execute(self, context: Context) -> Any:
        data = pd.read_csv(self.source_file)

        data["atccode"] = data["atccode"].astype("string")
        data["drug"] = data["drug"].astype("string")

        data.to_json(
            self.destination_file, orient="records", force_ascii=False, indent=2
        )


class ClinicalTrialsSilverOperator(BaseOperator):
    def __init__(
        self,
        source_file: str,
        destination_file: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_file = source_file
        self.destination_file = destination_file

    def execute(self, context: Context) -> Any:
        data = pd.read_csv(self.source_file)

        # Standardize
        data = data.rename(columns={"scientific_title": "title"})

        data["id"] = utils.clean_id(data["id"])
        data["title"] = utils.clean_title(data["title"])
        data["date"] = utils.clean_date(data["date"])
        data["journal"] = utils.clean_journal(data["journal"])

        # This data cannot be processed
        data = data.drop(data[data["title"] == ""].index)
        data = data.drop(data[data["journal"] == ""].index)

        data.to_json(
            self.destination_file,
            orient="records",
            force_ascii=False,
            indent=2,
        )


class PubmedMergeOperator(BaseOperator):
    def __init__(
        self,
        source_files: List[str],
        destination_file: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_files = source_files
        self.destination_file = destination_file

    def execute(self, context: Context) -> Any:
        data_to_concat = []

        for source_file in self.source_files:
            if source_file.endswith(".csv"):
                data = pd.read_csv(source_file)
                data_to_concat.append(data)

            elif source_file.endswith(".json"):
                with open(source_file) as f:
                    # json5 parses trailing commas found in pubmed files
                    data = json5.loads(f.read())
                data_to_concat.append(pd.DataFrame.from_dict(data))  # type: ignore

            else:
                # Do not let failures go undetected
                raise ValueError("Expecting either csv or json file")

        merged_data = pd.concat(data_to_concat)
        merged_data.to_json(
            self.destination_file, orient="records", force_ascii=False, indent=2
        )


class PubmedSilverOperator(BaseOperator):
    def __init__(
        self,
        source_file: str,
        destination_file: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.source_file = source_file
        self.destination_file = destination_file

    def execute(self, context: Context) -> Any:
        data = pd.read_json(self.source_file)

        data["id"] = utils.clean_id(data["id"])
        data["title"] = utils.clean_title(data["title"])
        data["date"] = utils.clean_date(data["date"])
        data["journal"] = utils.clean_journal(data["journal"])

        # This data could not be processed
        data = data.drop(data[data["title"] == ""].index)
        data = data.drop(data[data["journal"] == ""].index)

        data.to_json(
            self.destination_file,
            orient="records",
            force_ascii=False,
            indent=2,
        )


class DrugGraphGoldOperator(BaseOperator):
    def __init__(
        self,
        drug_source_file: str,
        clinical_trials_file: str,
        pubmed_file: str,
        destination_file: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.drug_source_file = drug_source_file
        self.clinical_trials_file = clinical_trials_file
        self.pubmed_file = pubmed_file
        self.destination_file = destination_file

    def get_drug_mapping(
        self,
        drugs: pd.DataFrame,
        clinical_trials: pd.DataFrame,
        pubmed: pd.DataFrame,
    ) -> Dict[str, Any]:
        drug_mapping = {}

        for _, drug_row in drugs.iterrows():
            quoting_ct = clinical_trials[
                clinical_trials["title"].str.contains(
                    drug_row["drug"], flags=re.IGNORECASE, regex=True
                )
            ]

            quoting_pubmed = pubmed[
                pubmed["title"].str.contains(
                    drug_row["drug"], flags=re.IGNORECASE, regex=True
                )
            ]

            drug_mapping[drug_row["atccode"]] = {
                "name": drug_row["drug"],
                "clinical_trial_id": quoting_ct["id"].tolist(),
                "pubmed_id": quoting_pubmed["id"].tolist(),
            }

        return drug_mapping

    def get_clinical_trial_mapping(
        self, clinical_trials: pd.DataFrame
    ) -> Dict[str, Any]:
        clinical_trials_mapping = {}

        for _, clinical_trial_row in clinical_trials.iterrows():
            clinical_trials_mapping[clinical_trial_row["id"]] = {
                "journal": clinical_trial_row["journal"],
                "date": clinical_trial_row["date"],
            }

        return clinical_trials_mapping

    def get_pubmed_mapping(self, pubmed: pd.DataFrame) -> Dict[str, Any]:
        pubmed_mapping = {}

        for _, pubmed_row in pubmed.iterrows():
            pubmed_mapping[pubmed_row["id"]] = {
                "journal": pubmed_row["journal"],
                "date": pubmed_row["date"],
            }

        return pubmed_mapping

    def get_journal_mapping(
        self,
        drugs: pd.DataFrame,
        clinical_trials: pd.DataFrame,
        pubmed: pd.DataFrame,
    ) -> Dict[str, Any]:
        journal_mapping = defaultdict(list)

        # Note: this doesn't protect against the same article published in different journals.
        publications = pd.concat([clinical_trials, pubmed])

        for _, drug_row in drugs.iterrows():
            quoting_publications = publications[
                publications["title"].str.contains(
                    drug_row["drug"], flags=re.IGNORECASE, regex=True
                )
            ]
            for _, publication_row in quoting_publications.iterrows():
                # It is possible to record multiple times one drug quoted in the same journal
                # for one day. This enables to perform fine-grained analytics afterward.
                # A drug name quoted multiple times in the same title is counts only for one here.
                # We data engineers need use cases to take appropriate modeling decisions.
                journal_mapping[publication_row["journal"]].append(
                    {"drug": drug_row["drug"], "date": publication_row["date"]}
                )

        return journal_mapping

    def execute(self, context: Context) -> Any:
        drug_graph = {}

        drug_data = pd.read_json(self.drug_source_file)
        clinical_trials_data = pd.read_json(self.clinical_trials_file)
        pubmed_data = pd.read_json(self.pubmed_file)

        clinical_trials_data["date"] = clinical_trials_data["date"].astype("string")
        pubmed_data["date"] = pubmed_data["date"].astype("string")

        drug_graph["drug"] = self.get_drug_mapping(
            drug_data, clinical_trials_data, pubmed_data
        )
        drug_graph["clinical_trial"] = self.get_clinical_trial_mapping(
            clinical_trials_data
        )
        drug_graph["pubmed"] = self.get_pubmed_mapping(pubmed_data)
        drug_graph["journal"] = self.get_journal_mapping(
            drug_data, clinical_trials_data, pubmed_data
        )

        with open(self.destination_file, "w+") as f:
            json.dump(drug_graph, f, indent=2, ensure_ascii=False)
