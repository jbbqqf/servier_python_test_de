from operator_drug import (
    ClinicalTrialsSilverOperator,
    CopyFileOperator,
    DrugGraphGoldOperator,
    DrugsSilverOperator,
    PubmedMergeOperator,
    PubmedSilverOperator,
)


def test_clinical_trials_silver_operator() -> None:
    # Given
    ClinicalTrialsSilverOperator(task_id="test", source_file="a", destination_file="b")

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_copy_file_operator() -> None:
    # Given
    CopyFileOperator(
        task_id="test",
        source_folder="a",
        source_path="b",
        destination_folder="c",
        destination_path="d",
    )

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_drug_graph_gold_operator_operator() -> None:
    # Given
    DrugGraphGoldOperator(task_id="test")

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_drugs_silver_operator() -> None:
    # Given
    DrugsSilverOperator(task_id="test", source_file="a", destination_file="b")

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_pubmed_merge_silver_operator() -> None:
    # Given
    PubmedMergeOperator(task_id="test", source_files=["a", "b"], destination_file="c")

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_pubmed_silver_operator() -> None:
    # Given
    PubmedSilverOperator(task_id="test", source_file="a", destination_file="b")

    # When, Then
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """
