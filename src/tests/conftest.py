import pytest
import sys
from airflow.configuration import conf
from typing import Generator


@pytest.fixture(scope="session")
def insert_dags_folder_in_path() -> Generator:
    sys.path.insert(0, conf.get("core", "dags_folder"))
    yield
