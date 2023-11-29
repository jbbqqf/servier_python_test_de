import pytest
from typing import Any
import utils
import numpy as np


@pytest.mark.parametrize("id_", ["", 1, "abcd", np.nan])
def test_ensure_id(id_: Any) -> None:
    # When
    transformed_id = utils.ensure_id(id_)

    # Then
    assert isinstance(transformed_id, str)


@pytest.mark.parametrize(
    "string, expected_cleaned_string",
    [
        (" \\\\xc3\\\\xc3", " "),
        ("Laminoplasty or \\xc3\\xb1 Laminectomy", "Laminoplasty or Laminectomy"),
        ("nursing\\xc3\\x28", "nursing"),
        ("nursing", "nursing"),
    ],
)
def test_clean_hexadecimal_patterns(string: str, expected_cleaned_string: str) -> None:
    # When
    cleaned_pattern = utils.clean_hexadecimal_patterns(string)

    # Then
    assert cleaned_pattern == expected_cleaned_string


def test_fuzzy_string_to_iso8601() -> None:
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_clean_id() -> None:
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_clean_title() -> None:
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_clean_date() -> None:
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """


def test_clean_journal() -> None:
    """
    I didn't take the time to implement this test because the rest
    of the technical test was already heavy.
    """
