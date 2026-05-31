from collections.abc import Callable
from dataclasses import dataclass

type BinaryOperation = Callable[[float, float], float]


class UnsupportedOperationError(ValueError):
    """指定された電卓の演算が登録されていない場合に送出される例外。"""


@dataclass(frozen=True)
class Operation:
    key: str
    label: str
    symbol: str
    calculate: BinaryOperation


def add(left: float, right: float) -> float:
    """2つの数値の和を返す。"""
    return left + right


def subtract(left: float, right: float) -> float:
    """2つの数値の差を返す。"""
    return left - right


def multiply(left: float, right: float) -> float:
    """2つの数値の積を返す。"""
    return left * right


def divide(left: float, right: float) -> float:
    """2つの数値の商を返す。"""
    return left / right


OPERATIONS: dict[str, Operation] = {
    "add": Operation(key="add", label="足し算", symbol="+", calculate=add),
    "subtract": Operation(key="subtract", label="引き算", symbol="-", calculate=subtract),
    "multiply": Operation(key="multiply", label="掛け算", symbol="x", calculate=multiply),
    "divide": Operation(key="divide", label="割り算", symbol="÷", calculate=divide),
}


def calculate(left: float, right: float, operation_key: str = "add") -> float:
    operation = OPERATIONS.get(operation_key)
    if operation is None:
        raise UnsupportedOperationError(f"Unsupported operation: {operation_key}")

    return operation.calculate(left, right)
