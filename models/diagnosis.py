"""
Contains all the database models for the diagnosis module.
"""

from beanie import PydanticObjectId

from beanie import Document
from pydantic import Field, field_serializer
from typing import Annotated


class Diagnosis(Document):
    """Diagnosis Model"""
    diagnosed_user_id: Annotated[str, Field(description="The ID of the user who received the diagnosis", serialization_alias="diagnosedUserId")]
    primary_diagnosis: Annotated[str, Field(description="The primary diagnosis", serialization_alias="primaryDiagnosis")]
    secondary_diagnoses: Annotated[list[str], Field(description="List of secondary diagnoses", default_factory=list, serialization_alias="secondaryDiagnoses")]
    description: Annotated[str, Field(description="Detailed description of the diagnosis", serialization_alias="description")]
    precautions: Annotated[list[str], Field(description="List of precautions to be taken", default_factory=list, serialization_alias="precautions")]
    severity_assessment: Annotated[str, Field(description="Assessment of the severity of the diagnosis", serialization_alias="severityAssessment")]
    initial_symptom: Annotated[str, Field(description="Initial symptom reported by the user", default=None, serialization_alias="initialSymptom")]
    additional_symptoms: Annotated[list[str], Field(description="List of additional symptoms reported by the user", default_factory=list, serialization_alias="additionalSymptoms")]
    days_experiencing: Annotated[int, Field(description="Number of days the user has been experiencing symptoms", default=0, serialization_alias="daysExperiencingSymptoms")]

    @field_serializer("id")
    def convert_pydantic_object_id_to_string(self, id: PydanticObjectId) -> str:
        return str(id)