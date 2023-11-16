from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class OuterData(BaseModel):
    text: str


class AnswerClassification(BaseModel):
    category: str
    theme: str
