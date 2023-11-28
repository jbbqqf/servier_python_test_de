from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
import pandas as pd
import json5
import shutil
from typing import Any
import os
import constant


class CopyFileOperator(BaseOperator):
    # TODO: document that the API is similar to GCStoGCSOperator
    def __init__(
        self,
        source_folder,
        source_path,
        destination_folder,
        destination_path,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.source_folder = source_folder
        self.source_path = source_path
        self.destination_folder = destination_folder
        self.destination_path = destination_path

    def execute(self, context) -> Any:
        shutil.copyfile(
            os.path.join(self.source_folder, self.source_path),
            os.path.join(self.destination_folder, self.destination_path),
        )


class DrugsSilverOperator(BaseOperator):
    # TODO: make reusable with parameters
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        data = pd.read_csv(constant.BRONZE_DRUGS_FILE)
        data["drug"] = data["drug"].str.lower()
        data.to_json(
            constant.SILVER_DRUGS_FILE, orient="records", force_ascii=False, indent=2
        )


class ClinicalTrialsSilverOperator(BaseOperator):
    # TODO: make reusable with parameters
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        bronze_data = pd.read_csv(constant.BRONZE_CLINICAL_TRIALS_FILE)
        # TODO: clean and filter
        bronze_data.to_json(
            constant.SILVER_CLINICAL_TRIALS_FILE,
            orient="records",
            force_ascii=False,
            indent=2,
        )


class PubmedSilverOperator(BaseOperator):
    # TODO: make reusable with parameters
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        bronze_a_data = pd.read_csv(constant.BRONZE_PUBMED_A_FILE)
        with open(constant.BRONZE_PUBMED_B_FILE) as f:
            bronze_json_data = json5.loads(f.read())
        bronze_b_data = pd.DataFrame.from_dict(bronze_json_data)
        # TODO: clean and filter
        bronze_data = pd.concat([bronze_a_data, bronze_b_data])
        bronze_data.to_json(
            constant.SILVER_PUBMED_FILE, orient="records", force_ascii=False, indent=2
        )


class DrugGraphGoldOperator(BaseOperator):
    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        # TODO: implement
        pass
