from datetime import datetime

from pydantic import BaseModel


class OrderEvent(BaseModel):
    description: str
    timestamp: datetime


class Order(BaseModel):
    id: str
    status: str
    expected_delivery: datetime
    events: list[OrderEvent]


class InvestigationRequest(BaseModel):
    question: str
