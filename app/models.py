from pydantic import BaseModel, field_validator
from typing import Optional

class ScrapeSettings(BaseModel):
    max_pages: int = 5
    proxy: Optional[str] = None

    @field_validator("max_pages")
    def validate_max_pages(cls, value):
        if value < 1:
            raise ValueError("max_pages must be at least 1")
        return value

    @field_validator("proxy")
    def validate_proxy(cls, value):
        if value and not value.startswith("http"):
            raise ValueError("proxy must be a valid URL starting with http or https")
        return value
