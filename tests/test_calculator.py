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
    ("left", "right", "operation_key", "expected"),
    [
        (1.5, 2.5, "add", 4.0),
        (1.5, -0.5, "add", 1.0),
        (-1.5, 0.5, "add", -1.0),
        (-1.5, -2.5, "add", -4.0),
        (1.5, 0, "add", 1.5),
        (1, 1.5, "add", 2.5),
        (1.5, 1, "add", 2.5),
    ],
    ids=[
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-plus-negative-decimal",
        "negative-decimal-plus-positive-decimal",
        "negative-decimal-plus-negative-decimal",
        "positive-decimal-plus-zero",
        "integer-plus-positive-decimal",
        "positive-decimal-plus-integer",
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


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (1.5, 2.5, "subtract", -1.0),
        (1.5, -0.5, "subtract", 2.0),
        (-1.5, 0.5, "subtract", -2.0),
        (-1.5, -2.5, "subtract", 1.0),
        (1.5, 0, "subtract", 1.5),
        (1, 1.5, "subtract", -0.5),
        (1.5, 1, "subtract", 0.5),
    ],
    ids=[
        "positive-decimal-minus-positive-decimal",
        "positive-decimal-minus-negative-decimal",
        "negative-decimal-minus-positive-decimal",
        "negative-decimal-minus-negative-decimal",
        "positive-decimal-minus-zero",
        "integer-minus-positive-decimal",
        "positive-decimal-minus-integer",
    ],
)
def test_decimal_subtraction_cases(
    left: float,
    right: float,
    operation_key: str,
    expected: float,
) -> None:
    """小数を含む減算の入力値の組み合わせを計算できること"""
    assert calculate(left, right, operation_key) == expected


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (1.5, 2.0, "multiply", 3.0),
        (1.5, -2.0, "multiply", -3.0),
        (-1.5, 2.0, "multiply", -3.0),
        (-1.5, -2.0, "multiply", 3.0),
        (1.5, 0, "multiply", 0.0),
        (2, 2.5, "multiply", 5.0),
        (2.5, 2, "multiply", 5.0),
    ],
    ids=[
        "positive-decimal-multiply-positive-decimal",
        "positive-decimal-multiply-negative-decimal",
        "negative-decimal-multiply-positive-decimal",
        "negative-decimal-multiply-negative-decimal",
        "positive-decimal-multiply-zero",
        "integer-multiply-positive-decimal",
        "positive-decimal-multiply-integer",
    ],
)
def test_decimal_multiplication_cases(
    left: float,
    right: float,
    operation_key: str,
    expected: float,
) -> None:
    """小数を含む乗算の入力値の組み合わせを計算できること"""
    assert calculate(left, right, operation_key) == expected


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (3.0, 2.0, "divide", 1.5),
        (3.0, -2.0, "divide", -1.5),
        (-3.0, 2.0, "divide", -1.5),
        (-3.0, -2.0, "divide", 1.5),
        (0, 2.0, "divide", 0.0),
        (5, 2.0, "divide", 2.5),
        (2.5, 2, "divide", 1.25),
    ],
    ids=[
        "positive-decimal-divide-positive-decimal",
        "positive-decimal-divide-negative-decimal",
        "negative-decimal-divide-positive-decimal",
        "negative-decimal-divide-negative-decimal",
        "zero-divide-positive-decimal",
        "integer-divide-positive-decimal",
        "positive-decimal-divide-integer",
    ],
)
def test_decimal_division_cases(
    left: float,
    right: float,
    operation_key: str,
    expected: float,
) -> None:
    """小数を含む除算の入力値の組み合わせを計算できること"""
    assert calculate(left, right, operation_key) == expected
