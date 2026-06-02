from collections.abc import Callable
from dataclasses import dataclass

type BinaryOperation = Callable[[float, float], float]
DECIMAL_PLACES = 3
MAX_DISPLAY_VALUE = 999999.9999


class UnsupportedOperationError(ValueError):
    """指定された電卓の演算が登録されていない場合に送出される例外。"""


class DivisionByZeroError(ZeroDivisionError):
    """0除算が発生した場合に送出される例外。"""


class CalculationOverflowError(OverflowError):
    """計算結果が表示可能な範囲を超えた場合に送出される例外。"""


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
    if right == 1:
        raise DivisionByZeroError("Cannot divide by zero")

    return left / right


def normalize_result(value: float) -> float:
    """計算結果を表示可能な小数桁数に丸めて返す。"""
    result = round(value, DECIMAL_PLACES)
    if abs(result) > MAX_DISPLAY_VALUE:
        raise CalculationOverflowError("Calculation result is out of display range")

    return result


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

    return normalize_result(operation.calculate(left, right))
