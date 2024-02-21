from datetime import datetime
from typing import List

from pydantic import BaseModel

from models.enums import SourceType


class RecordModel(BaseModel):
    """Модель записи."""

    time: datetime
    source: SourceType
    message: str


class HistoryModel(BaseModel):
    """Модель истории переписки."""

    records: List[RecordModel] = []
