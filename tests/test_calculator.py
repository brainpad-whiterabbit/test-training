import pytest

from training.calculator import calculate, DivisionByZeroError


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
        "negative-plus-negative",
        "negative-plus-positive",
        "positive-plus-negative",
        "positive-plus-positive",
        "includes-zero",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


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
        (-1, -1, 1),
        (-1, 3, -3),
        (1, -3, -3),
        (5, 1, 5),
        (0, 1, 0),
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
        (-1, -1, 1),
        (-1, 3, -0.333),
        (1, -3, -0.333),
        (5, 1, 5),
        (0, 1, 0),
        (999999, 1, 999999),
        (-999999, 1, -999999),
    ],
    ids=[
        "negative-divide-negative",
        "negative-divide-positive",
        "positive-divide-negative",
        "positive-divide-positive",
        "includes-zero",
        "includes-maximum",
        "includes-minimum",
    ],
)
def test_division_cases(left: float, right: float, expected: float) -> None:
    """除算の代表的な入力値の組み合わせを計算できること（小数は小数点第3位で丸められる）"""
    assert calculate(left, right, "divide") == expected


def test_division_by_zero() -> None:
    """0除算で DivisionByZeroError が送出されること"""
    with pytest.raises(DivisionByZeroError):
        calculate(1, 0, "divide")
