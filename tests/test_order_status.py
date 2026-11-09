from datetime import datetime
from zoneinfo import ZoneInfo

from app.main import load_orders
from app.services.order_status import classify_order_status, get_order_status

FORTALEZA = ZoneInfo("America/Fortaleza")


def test_order_is_on_time_with_more_than_24_hours_remaining():
    current_time = datetime(2026, 11, 9, 17, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "IN_TRANSIT",
        expected_delivery,
        current_time
    )

    assert result == "NO_PRAZO"


def test_order_is_on_time_with_exactly_24_hours_remaining():
    current_time = datetime(2026, 11, 9, 18, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "IN_TRANSIT",
        expected_delivery,
        current_time
    )

    assert result == "NO_PRAZO"


def test_order_is_at_risk_with_less_than_24_hours_remaining():
    current_time = datetime(2026, 11, 9, 18, 1, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "IN_TRANSIT",
        expected_delivery,
        current_time
    )

    assert result == "EM_RISCO"


def test_order_is_late_at_deadline():
    current_time = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "IN_TRANSIT",
        expected_delivery,
        current_time
    )

    assert result == "ATRASADO"


def test_delivered_order_on_time():
    current_time = datetime(2026, 11, 10, 19, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)
    delivered_at = datetime(2026, 11, 10, 17, 30, tzinfo=FORTALEZA)

    result = classify_order_status(
        "DELIVERED",
        expected_delivery,
        current_time,
        delivered_at
    )

    assert result == "ENTREGUE"


def test_delivered_order_late():
    current_time = datetime(2026, 11, 10, 20, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)
    delivered_at = datetime(2026, 11, 10, 18, 30, tzinfo=FORTALEZA)

    result = classify_order_status(
        "DELIVERED",
        expected_delivery,
        current_time,
        delivered_at
    )

    assert result == "ENTREGUE_COM_ATRASO"


def test_delivered_order_without_delivery_timestamp():
    current_time = datetime(2026, 11, 10, 20, 0, tzinfo=FORTALEZA)
    expected_delivery = datetime(2026, 11, 10, 18, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "DELIVERED",
        expected_delivery,
        current_time
    )

    assert result == "INDETERMINADO"


def test_missing_delivery_deadline():
    current_time = datetime(2026, 11, 9, 17, 0, tzinfo=FORTALEZA)

    result = classify_order_status(
        "IN_TRANSIT",
        None,
        current_time
    )

    assert result == "INDETERMINADO"


def test_classify_real_delivered_order():
    orders = load_orders()

    order = next(
        order for order in orders
        if order.id == "98766"
    )

    current_time = datetime(
        2026, 11, 9, 10, 0,
        tzinfo=FORTALEZA
    )

    result = get_order_status(order, current_time)

    assert result == "ENTREGUE"
