from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ServiceSchema(BaseModel):
    service_id: str = Field(..., unique=True)
    organization_id: str
    service_name: str
    service_description: str
    service_status: Optional[str] = "Operational"
    start_date: Optional[datetime] = Field(default_factory=datetime.now)
