from datetime import datetime, timedelta

from app.models import Order


def classify_order_status(
    order_status: str,
    expected_delivery: datetime | None,
    current_time: datetime,
    delivered_at: datetime | None = None
) -> str:
    if order_status == "DELIVERED":
        if expected_delivery is None or delivered_at is None:
            return "INDETERMINADO"

        if (
            expected_delivery.utcoffset() is None
            or delivered_at.utcoffset() is None
        ):
            return "INDETERMINADO"

        if delivered_at > expected_delivery:
            return "ENTREGUE_COM_ATRASO"

        return "ENTREGUE"

    if expected_delivery is None:
        return "INDETERMINADO"

    if (
        current_time.utcoffset() is None
        or expected_delivery.utcoffset() is None
    ):
        return "INDETERMINADO"

    if current_time >= expected_delivery:
        return "ATRASADO"

    remaining_time = expected_delivery - current_time

    if remaining_time < timedelta(hours=24):
        return "EM_RISCO"

    return "NO_PRAZO"


def get_order_status(
    order: Order,
    current_time: datetime
) -> str:

    delivered_at = next(
        (
            event.timestamp
            for event in order.events
            if event.description.strip().lower() == "order delivered"
        ),
        None
    )

    return classify_order_status(
        order.status,
        order.expected_delivery,
        current_time,
        delivered_at
    )