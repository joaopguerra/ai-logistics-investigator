import json

from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.models import Order


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "orders.json"
)

app = FastAPI(
    title="AI Logistics Investigator",
    description="API for logistics order investigation",
    version="1.0.0"
)


def load_orders() -> list[Order]:
    with DATA_FILE.open(encoding="utf-8") as file:
        data = json.load(file)

    return [
        Order.model_validate(order)
        for order in data["orders"]
    ]


def find_order(order_id: str) -> Order | None:
    orders = load_orders()

    return next(
        (
            order
            for order in orders
            if order.id == order_id
        ),
        None
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "UP"}


@app.get("/orders", response_model=list[Order])
def get_orders() -> list[Order]:
    return load_orders()


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str) -> Order:
    order = find_order(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order