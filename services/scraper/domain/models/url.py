from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class FetchStatus(Enum):
    CAPTCHA: str = "captcha"
    FAILED: str = "fail to fetch"
    NOT_FOUND: str = "not found"
    SUCCESSFUL: str = "successful"


class OuterData(BaseModel):
    urls: List[str]


class AnswerClassification(BaseModel):
    category: str
    theme: str


class AnswerDataFetched(BaseModel):
    url: str
    status: FetchStatus
    content: Optional[str] = None
    meta_inf: Optional[str] = None


class AnswerDataClassified(AnswerDataFetched):
    category: Optional[AnswerClassification] = None
    related_links: Optional[List[str]] = None
