from collections.abc import Callable
from dataclasses import dataclass

type BinaryOperation = Callable[[float, float], float]


class UnsupportedOperationError(ValueError):
    """Raised when a requested calculator operation is not registered."""


@dataclass(frozen=True)
class Operation:
    key: str
    label: str
    symbol: str
    calculate: BinaryOperation


def add(left: float, right: float) -> float:
    """Return the sum of two numbers."""
    return left + right


OPERATIONS: dict[str, Operation] = {
    "add": Operation(key="add", label="足し算", symbol="+", calculate=add),
}


def calculate(left: float, right: float, operation_key: str = "add") -> float:
    operation = OPERATIONS.get(operation_key)
    if operation is None:
        raise UnsupportedOperationError(f"Unsupported operation: {operation_key}")

    return operation.calculate(left, right)
