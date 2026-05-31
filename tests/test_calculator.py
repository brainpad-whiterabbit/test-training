import pytest

from training.calculator import calculate


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
        (-1, -3, 2),
        (-1, 1, -2),
        (1, -1, 2),
        (5, 1, 4),
        (0, 1, -1),
        (999999, 1, 999998),
        (-999999, 1, -1000000),
        (999999, 999999, 0),
        (-999999, -999999, 0),
    ],
    ids=[
        "negative-minus-negative",
        "negative-minus-positive",
        "positive-minus-negative",
        "positive-minus-positive",
        "includes-zero",
        "includes-maximum",
        "includes-minimum",
        "maximum-minus-maximum",
        "minimum-minus-minimum",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-2, -5, 10),
        (-2, 5, -10),
        (2, -5, -10),
        (5, 5, 25),
        (0, 5, 0),
        (999999, 1, 999999),
        (-999999, 1, -999999),
    ],
    ids=[
        "negative-times-negative",
        "negative-times-positive",
        "positive-times-negative",
        "positive-times-positive",
        "includes-zero",
        "includes-maximum",
        "includes-minimum",
    ],
)
def test_multiplication_cases(left: float, right: float, expected: float) -> None:
    """乗算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "multiply") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-10, -2, 5),
        (-10, 2, -5),
        (10, -2, -5),
        (10, 2, 5),
        (0, 10, 0),
        (999999, 9, 111111),
        (-999999, 9, -111111),
        (999999, 999999, 1),
        (-999999, -999999, 1),
        (999999, -999999, -1),
    ],
    ids=[
        "negative-divided-by-negative",
        "negative-divided-by-positive",
        "positive-divided-by-negative",
        "positive-divided-by-positive",
        "zero-divided-by-positive",
        "includes-maximum",
        "includes-minimum",
        "maximum-divided-by-maximum",
        "minimum-divided-by-minimum",
        "maximum-divided-by-minimum",
    ],
)
def test_division_cases(left: float, right: float, expected: float) -> None:
    """除算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "divide") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (10, 0, "Error"),
        (-10, 0, "Error"),
        (0, 0, "Error"),
        (999999, 0, "Error"),
        (-999999, 0, "Error"),
    ],
    ids=[
        "positive-divided-by-zero",
        "negative-divided-by-zero",
        "zero-divided-by-zero",
        "maximum-divided-by-zero",
        "minimum-divided-by-zero",
    ],
)
def test_division_by_zero_cases(left: float, right: float, expected: str) -> None:
    """0除算時にErrorを返すこと"""
    assert calculate(left, right, "divide") == expected


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (1.5, 2.5, "add", 4.0),
        (1.5, 2.5, "subtract", -1.0),
        (1.5, 2.5, "multiply", 3.75),
        (1.5, 2.5, "divide", 0.6),
        (1.5, -0.5, "add", 1.0),
        (-1.5, 0.5, "add", -1.0),
        (-1.5, -2.5, "add", -4.0),
        (1.5, 0, "add", 1.5),
        (1, 1.5, "add", 2.5),
        (1.5, 1, "add", 2.5),
        (999999.9999, 0.0001, "subtract", 999999.9998),
    ],
    ids=[
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-minus-positive-decimal",
        "positive-decimal-times-positive-decimal",
        "positive-decimal-divided-by-positive-decimal",
        "positive-decimal-plus-negative-decimal",
        "negative-decimal-plus-positive-decimal",
        "negative-decimal-plus-negative-decimal",
        "positive-decimal-plus-zero",
        "integer-plus-positive-decimal",
        "positive-decimal-plus-integer",
        "large-decimal-minus-small-decimal",
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
