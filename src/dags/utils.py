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
      - "\\xc3"
      - "\xc3"
      - "\x28"

    In theory, we're supposed to be informed of the encoding. It's not possible to guess it.

    That being said, in real life, it's optimistic to expect being informed of the encoding.

    The command `chardetect clinical_trials.csv` return "utf-8 with confidence 0.87625". It
    would make sense for that file to be utf-8, because it's popular and works for some words
    in the file.

    Unless I missed something, those hexadecimal patterns are data quality issues and not
    a mysterious encoding puzzle to solve. This is why I wrote some this function to simply
    remove it.
    """

    first_hexadecimal_pattern = r"\\\\x[0-9a-fA-F]{2} ?"
    second_hexadecimal_pattern = r"\\x[0-9a-fA-F]{2} ?"

    first_cleaned_string = re.sub(first_hexadecimal_pattern, "", string)
    second_cleaned_string = re.sub(second_hexadecimal_pattern, "", first_cleaned_string)

    return second_cleaned_string


def fuzzy_string_to_iso8601(string: str) -> str:
    return parse(string, fuzzy=True).date().isoformat()


def clean_id(s: pd.Series) -> pd.Series:
    # We don't need an authentic id to derive value from our data, so if we detect
    # a missing id we can fix it.
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
    s = s.fillna(value="")  # Easier to only have to deal with strings
    s = s.str.strip()
    s = s.apply(clean_hexadecimal_patterns)
    s = s.astype("string")
    return s
