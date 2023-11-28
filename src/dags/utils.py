from typing import Optional
from uuid import uuid4


def ensure_id(id_: Optional[str]) -> str:
    return id_ if id_ else str(uuid4())
