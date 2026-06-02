import pytest

from training.calculator import CalculationOverflowError, DivisionByZeroError, calculate


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
        (-1.5, -3.2, 1.7),
        (-1.5, 1.2, -2.7),
        (1.5, -1.2, 2.7),
        (4.5, 1.2, 3.3),
        (0.0, 1.5, -1.5),
        (1.5, 0.25, 1.25),
        (2.0, 1.5, 0.5),
        (1.5, 2.0, -0.5),
    ],
    ids=[
        "negative-decimal-minus-negative-decimal",
        "negative-decimal-minus-positive-decimal",
        "positive-decimal-minus-negative-decimal",
        "positive-decimal-minus-positive-decimal",
        "zero-minus-positive-decimal",
        "different-fractional-digits",
        "integer-minus-decimal",
        "decimal-minus-integer",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (999999.99, 1.1, 999998.89),
        (999999.99, 999999.99, 0.0),
        (-999999.99, -999999.99, 0.0),
        (0.3, 0.1, 0.2),
    ],
    ids=[
        "max-value-minus-small-decimal",
        "max-value-minus-max-value",
        "min-value-minus-min-value",
        "floating-point-precision",
    ],
)
def test_subtraction_boundary_and_precision_cases(
    left: float, right: float, expected: float
) -> None:
    """境界値と精度に関する減算を計算できること"""
    assert calculate(left, right, "subtract") == expected


def test_subtraction_overflow_raises_error() -> None:
    """Overflow時にオーバーフロー例外が発生すること"""
    with pytest.raises(CalculationOverflowError):
        calculate(999999.99, -1.0, "subtract")


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
    ("left", "right", "expected"),
    [
        (-2, -3, 6),
        (-2, 3, -6),
        (2, 3, 6),
        (5, 0, 0),
        (5, 1, 5),
        (2.5, 2.0, 5.0),
        (-1.5, 2.0, -3.0),
    ],
    ids=[
        "negative-times-negative",
        "negative-times-positive",
        "positive-times-positive",
        "multiply-by-zero",
        "multiply-by-one",
        "decimal-multiplication",
        "negative-decimal-multiplication",
    ],
)
def test_multiplication_cases(left: float, right: float, expected: float) -> None:
    """乗算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "multiply") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-6, -2, 3),
        (-6, 2, -3),
        (6, -2, -3),
        (6, 2, 3),
        (0, 5, 0),
        (5.0, 2.0, 2.5),
        (-3.0, 2.0, -1.5),
    ],
    ids=[
        "negative-divide-negative",
        "negative-divide-positive",
        "positive-divide-negative",
        "positive-divide-positive",
        "zero-divide-by-number",
        "decimal-division",
        "negative-decimal-division",
    ],
)
def test_division_cases(left: float, right: float, expected: float) -> None:
    """除算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "divide") == expected


def test_division_by_zero_raises_error() -> None:
    """0で除算するとエラーが発生すること"""
    with pytest.raises(DivisionByZeroError):
        calculate(5, 0, "divide")


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        (2.5, 2.0, "multiply", 5.0),
        (5.0, 2.0, "divide", 2.5),
        (0.1, 3, "multiply", 0.3),
        (1.5, 2.0, "subtract", -0.5),
        (1.5, 2.0, "add", 3.5),
    ],
    ids=[
        "decimal-multiplication",
        "decimal-division",
        "floating-point-precision",
        "decimal-subtraction",
        "decimal-addition",
    ],
)
def test_decimal_operations(
    left: float,
    right: float,
    operation_key: str,
    expected: float,
) -> None:
    """小数を含む四則演算を計算できること"""
    assert calculate(left, right, operation_key) == expected
