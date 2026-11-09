from datetime import date, datetime

from pydantic import BaseModel


class OrderEvent(BaseModel):
    description: str
    timestamp: datetime


class Order(BaseModel):
    id: str
    status: str
    expected_delivery: date
    events: list[OrderEvent]