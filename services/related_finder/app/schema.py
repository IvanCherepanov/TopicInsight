from typing import Optional, List

from pydantic import BaseModel


class UserInput(BaseModel):
    url: str
    text: Optional[str]


class RelatedSource(BaseModel):
    url: str
    list_url: List[str]

    def to_dict(self):
        return {
            "url": self.url,
            "list_url": self.list_url
        }
