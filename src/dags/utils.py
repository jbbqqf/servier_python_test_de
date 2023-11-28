import re
from typing import Any
from uuid import uuid4

import pandas as pd
from dateutil.parser import parse


def ensure_id(id_: Any) -> str:
    """
    Return a synthetic id if the value is not a string or an empty string.
    """
    return id_ if isinstance(id_, str) and bool(id_) else str(uuid4())


def clean_hexadecimal_patterns(string: str) -> str:
    """
    Remove:
      - "\\xc3"
      - "\\xb1 "
      - "\xc3"
      - "\x28"
    """

    first_hexadecimal_pattern = r"\\x[0-9a-fA-F]{2} ?"
    second_hexadecimal_pattern = r"\\\\x[0-9a-fA-F]{2} ?"

    first_cleaned_string = re.sub(first_hexadecimal_pattern, "", string)
    second_cleaned_string = re.sub(second_hexadecimal_pattern, "", first_cleaned_string)

    return second_cleaned_string


def fuzzy_string_to_iso8601(string: str) -> str:
    return parse(string, fuzzy=True).date().isoformat()


def clean_id(s: pd.Series) -> pd.Series:
    return s.apply(ensure_id).astype("string")


def clean_title(s: pd.Series) -> pd.Series:
    s = s.str.strip()
    s = s.apply(clean_hexadecimal_patterns)
    s = s.astype("string")
    return s


def clean_date(s: pd.Series) -> pd.Series:
    s = s.astype("string")  # Forces parsing
    s = s.apply(fuzzy_string_to_iso8601)
    s = s.astype("string")
    return s


def clean_journal(s: pd.Series) -> pd.Series:
    s = s.fillna(value="")
    s = s.str.strip()
    s = s.apply(clean_hexadecimal_patterns)
    s = s.astype("string")
    return s
