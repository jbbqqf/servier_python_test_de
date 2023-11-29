from airflow.models import DagBag


def test_get_import_errors() -> None:
    # Ensure dags can be imported
    dag_bag = DagBag(include_examples=False)
    assert not dag_bag.import_errors
