import pytest

from training.calculator import calculate


# ==========================================
# 加算（足し算）のテストケース
# ==========================================
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


# ==========================================
# 減算（引き算）のテストケース（Overflowを除外）
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1, -3, 2),
        (-1, 1, -2),
        (1, -1, 2),
        (1, 4, -3),
        (0, 1, -1),
        (999999, 1, 999998),
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
        "maximum-minus-maximum",
        "minimum-minus-minimum",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float | str) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


# ==========================================
# 小数・加算のテストケース
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1.1, -2.3, -3.4),
        (-1.2, 1.3, 0.1),
        (1.5, -1.2, 0.3),
        (1.2, 4.5, 5.7),
        (0.0, 1.2, 1.2),
        (-99.99, 0.01, -99.98),
        (99.99, -99.99, 0.0),
        (-99.99, 99.99, 0.0),
    ],
    ids=[
        "negative-plus-negative",
        "negative-plus-positive",
        "positive-plus-negative",
        "positive-plus-positive",
        "includes-zero",
        "includes-minimum",
        "maximum-plus-minimum",
        "minimum-plus-maximum",
    ],
)
def test_decimal_addition_cases(left: float, right: float, expected: float | str) -> None:
    """小数の加算ができること"""
    assert calculate(left, right, "add") == expected


# ==========================================
# 小数・減算のテストケース（Overflowを除外）
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1.1, -2.3, 1.2),
        (-1.2, 1.3, -2.5),
        (1.5, -1.2, 2.7),
        (1.2, 4.5, -3.3),
        (0.0, 1.2, -1.2),
        (99.99, 0.01, 99.98),
        (99.99, 99.99, 0.0),
        (-99.99, -99.99, 0.0),
    ],
    ids=[
        "negative-minus-negative",
        "negative-minus-positive",
        "positive-minus-negative",
        "positive-minus-positive",
        "includes-zero",
        "includes-maximum",
        "maximum-minus-maximum",
        "minimum-minus-minimum",
    ],
)
def test_decimal_subtraction_cases(left: float, right: float, expected: float | str) -> None:
    """小数の減算ができること"""
    assert calculate(left, right, "subtract") == expected


# ==========================================
# 乗算（掛け算）のテストケース
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-2, -3, 6),
        (-2, 3, -6),
        (2, -3, -6),
        (2, 3, 6),
        (0, 5, 0),
    ],
    ids=[
        "negative-times-negative",
        "negative-times-positive",
        "positive-times-negative",
        "positive-times-positive",
        "includes-zero",
    ],
)
def test_integer_multiplication_cases(left: int, right: int, expected: int) -> None:
    """整数の乗算ができること"""
    assert calculate(left, right, "multiply") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1.2, -2.0, 2.4),
        (-1.2, 1.5, -1.8),
        (1.5, -1.2, -1.8),
        (1.2, 2.5, 3.0),
        (0.0, 1.5, 0.0),
    ],
    ids=[
        "decimal-negative-times-negative",
        "decimal-negative-times-positive",
        "decimal-positive-times-negative",
        "decimal-positive-times-positive",
        "decimal-includes-zero",
    ],
)
def test_decimal_multiplication_cases(left: float, right: float, expected: float) -> None:
    """小数の乗算ができること"""
    assert calculate(left, right, "multiply") == expected


# ==========================================
# 除算（割り算）のテストケース
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-6, -2, 3),
        (-6, 2, -3),
        (6, -2, -3),
        (6, 2, 3),
        (0, 2, 0),
        (5, 0, ZeroDivisionError),
    ],
    ids=[
        "negative-div-negative",
        "negative-div-positive",
        "positive-div-negative",
        "positive-div-positive",
        "includes-zero-numerator",
        "zero-division",
    ],
)
def test_integer_division_cases(left: int, right: int, expected: int | type) -> None:
    """整数の除算ができること"""
    if expected == ZeroDivisionError:
        with pytest.raises(ZeroDivisionError):
            calculate(left, right, "divide")
    else:
        assert calculate(left, right, "divide") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-2.4, -1.2, 2.0),
        (-2.4, 1.2, -2.0),
        (2.4, -1.2, -2.0),
        (2.4, 1.2, 2.0),
        (0.0, 1.2, 0.0),
        (1.2, 0.0, ZeroDivisionError),
    ],
    ids=[
        "decimal-negative-div-negative",
        "decimal-negative-div-positive",
        "decimal-positive-div-negative",
        "decimal-positive-div-positive",
        "decimal-includes-zero-numerator",
        "decimal-zero-division",
    ],
)
def test_decimal_division_cases(left: float, right: float, expected: float | type) -> None:
    """小数の除算ができること"""
    if expected == ZeroDivisionError:
        with pytest.raises(ZeroDivisionError):
            calculate(left, right, "divide")
    else:
        assert calculate(left, right, "divide") == expected