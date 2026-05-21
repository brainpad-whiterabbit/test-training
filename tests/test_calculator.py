import pytest

from training import OPERATIONS, UnsupportedOperationError, add, calculate


def test_add_returns_sum() -> None:
    assert add(2, 3) == 5


def test_calculate_uses_addition_by_default() -> None:
    assert calculate(1.5, 2.25) == 3.75


def test_addition_operation_is_registered() -> None:
    operation = OPERATIONS["add"]

    assert operation.label == "足し算"
    assert operation.symbol == "+"
    assert operation.calculate(4, 6) == 10


def test_calculate_rejects_unknown_operation() -> None:
    with pytest.raises(UnsupportedOperationError):
        calculate(1, 2, "multiply")
