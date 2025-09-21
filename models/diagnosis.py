"""
Contains all the database models for the diagnosis module.
"""

from beanie import Document
from pydantic import Field
from typing import Annotated


class Diagnosis(Document):
    """Diagnosis Model"""
    diagnosed_user_id: Annotated[str, Field(description="The ID of the user who received the diagnosis", serialization_alias="diagnosedUserId")]
    primary_diagnosis: Annotated[str, Field(description="The primary diagnosis", serialization_alias="primaryDiagnosis")]
    secondary_diagnoses: Annotated[list[str], Field(description="List of secondary diagnoses", default_factory=list, serialization_alias="secondaryDiagnoses")]
    description: Annotated[str, Field(description="Detailed description of the diagnosis", serialization_alias="description")]
    precautions: Annotated[list[str], Field(description="List of precautions to be taken", default_factory=list, serialization_alias="precautions")]
    severity_assessment: Annotated[str, Field(description="Assessment of the severity of the diagnosis", serialization_alias="severityAssessment")]