from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class IncidentModel(BaseModel):
    incident_id: str = Field(..., unique=True)
    service_impacted: List[str] = Field(...)
    organization_id: str = Field(...)
    incident_name: str = Field(...)
    incident_description: str = Field(...)
    incident_status: str = Field(default="Operational")
    created_at: datetime = Field(default_factory=datetime.now)
