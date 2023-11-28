import os
import shutil
from typing import Any, List

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
    def __init__(
        self,
        source_file,
        destination_file,
        **kwargs,
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
        source_file,
        destination_file,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.source_file = source_file
        self.destination_file = destination_file

    def execute(self, context: Context) -> Any:
        data = pd.read_csv(self.source_file)

        data["id"] = utils.clean_id(data["id"])
        data["scientific_title"] = utils.clean_title(data["scientific_title"])
        data["date"] = utils.clean_date(data["date"])
        data["journal"] = utils.clean_journal(data["journal"])

        # This data cannot be processed
        data = data.drop(data[data["scientific_title"] == ""].index)
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
        **kwargs,
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
                data_to_concat.append(pd.DataFrame.from_dict(data))

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
        source_file,
        destination_file,
        **kwargs,
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

        # This data could not be processed (even if those cases have not been witnessed)
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
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        # TODO: implement
        pass
