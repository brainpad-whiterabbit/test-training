import pytest

from training.calculator import (
    OPERATIONS,
    UnsupportedOperationError,
    add,
    calculate,
    subtract,
)


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_subtract_returns_difference() -> None:
    assert subtract(8, 3) == 5


def test_calculate_uses_addition_by_default() -> None:
    assert calculate(1.5, 2.25) == 3.75


def test_calculate_uses_requested_subtraction() -> None:
    assert calculate(10, 4, "subtract") == 6


def test_addition_operation_is_registered() -> None:
    operation = OPERATIONS["add"]

    assert operation.label == "足し算"
    assert operation.symbol == "+"
    assert operation.calculate(4, 6) == 10


def test_subtraction_operation_is_registered() -> None:
    operation = OPERATIONS["subtract"]

    assert operation.label == "引き算"
    assert operation.symbol == "-"
    assert operation.calculate(9, 4) == 5


def test_calculate_rejects_unknown_operation() -> None:
    with pytest.raises(UnsupportedOperationError):
        calculate(1, 2, "multiply")
