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
    diagnosed_user_id: str
    initial_symptom: Annotated[
        str,
        Field(
            description="Initial symptom reported by the user",
            default=None,
            serialization_alias="initialSymptom",
        ),
    ]
    additional_symptoms: Annotated[
        list[str],
        Field(
            description="List of additional symptoms reported by the user",
            default_factory=list,
            serialization_alias="additionalSymptoms",
        ),
    ]
    days_experiencing: Annotated[
        int,
        Field(
            description="Number of days the user has been experiencing symptoms",
            default=0,
            serialization_alias="daysExperiencingSymptoms",
        ),
    ]