"""Request model for creating a new diagnosis.
"""

from pydantic import BaseModel, Field
from typing import Annotated


class DiagnosisCreateRequest(BaseModel):
    primary_diagnosis: str
    secondary_diagnosis: str | None
    confidence_level: str
    description: str
    precautions: Annotated[list[str], Field(description="List of precautions to take")]
    severity_assessment: str