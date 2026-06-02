import pytest

from training.calculator import DivisionByZeroError, calculate


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1, -1, -2),
        (-1, 3, 2),
        (1, -3, -2),
        (5, 1, 6),
        (0, 1, 1),
        (999999, -10, 999989),
        (-999999, 10, -999989),
    ],
    ids=[
        "negative-plus-negative",
        "negative-plus-positive",
        "positive-plus-negative",
        "positive-plus-positive",
        "includes-zero",
        "includes-maximum",
        "includes-minimum",
    ],
)
def test_addition_cases(left: float, right: float, expected: float) -> None:
    """加算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "add") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1, -1, 0),
        (-1, 3, -4),
        (1, -3, 4),
        (5, 1, 4),
        (0, 1, -1),
    ],
    ids=[
        "negative-minus-negative",
        "negative-minus-positive",
        "positive-minus-negative",
        "positive-minus-positive",
        "includes-zero",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 2, 4),
        (-2, -2, 4),
        (2, -2, -4),
        (2, 0, 0),
    ],
    ids=[
        "positive-times-positive",
        "negative-times-negative",
        "positive-times-negative",
        "includes-zero",
    ],
)
def test_multiplication_cases(left: float, right: float, expected: float) -> None:
    """掛け算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "multiply") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (4, 2, 2),
        (4, -2, -2),
        (-4, 2, -2),
        (0, 2, 0),
    ],
    ids=[
        "positive-divide-positive",
        "positive-divide-negative",
        "negative-divide-positive",
        "includes-zero",
    ],
)
def test_division_cases(left: float, right: float, expected: float) -> None:
    """割り算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "divide") == expected


def test_division_by_zero_raises_error() -> None:
    """0 で割ると DivisionByZeroError が発生すること"""
    with pytest.raises(DivisionByZeroError):
        calculate(1, 0, "divide")


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (1.5, 2.5, "add", 4.0),
        (1.5, -0.5, "add", 1.0),
        (-1.5, 0.5, "add", -1.0),
        (-1.5, -2.5, "add", -4.0),
        (1.5, 0, "add", 1.5),
        (1, 1.5, "add", 2.5),
        (1.5, 1, "add", 2.5),
        (1.5, 2.5, "subtract", -1.0),
        (1.5, -0.5, "subtract", 2.0),
        (2, 0.25, "multiply", 0.5),
        (0.5, 2, "divide", 0.25),
    ],
    ids=[
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-plus-negative-decimal",
        "negative-decimal-plus-positive-decimal",
        "negative-decimal-plus-negative-decimal",
        "positive-decimal-plus-zero",
        "integer-plus-positive-decimal",
        "positive-decimal-plus-integer",
        "positive-decimal-minus-positive-decimal",
        "positive-decimal-minus-negative-decimal",
        "integer-times-decimal",
        "decimal-divide-integer",
    ],
)
def test_decimal_cases(
    left: float,
    right: float,
    operation_key: str,
    expected: float,
) -> None:
    """小数を含む代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, operation_key) == expected
