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
        (1, 4, -3),
        (0, 1, -1),
        (999999, 1, 999998),
        (-999999, 1, "Overflow"),
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
def test_subtraction_cases(left: float, right: float, expected: float | str) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    # 加算の "add" に倣い、減算の第3引数は "sub" と仮定しています
    assert calculate(left, right, "subtract") == expected


# ==========================================
# 1. 加算（足し算）のテストケース
# ==========================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1.1, -2.3, -3.4),
        (-1.2, 1.3, 0.1),
        (1.5, -1.2, 0.3),
        (1.2, 4.5, 5.7),
        (0.0, 1.2, 1.2),
        (99.99, 0.01, "Overflow"),
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
        "includes-maximum",
        "includes-minimum",
        "maximum-plus-minimum",
        "minimum-plus-maximum",
    ],
)
def test_decimal_addition_cases(left: float, right: float, expected: float | str) -> None:
    """小数の加算ができること"""
    assert calculate(left, right, "add") == expected


# ==========================================
# 2. 減算（引き算）のテストケース
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
        (-99.99, 0.01, "Overflow"),
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
        "includes-minimum",
        "maximum-minus-maximum",
        "minimum-minus-minimum",
    ],
)
def test_decimal_subtraction_cases(left: float, right: float, expected: float | str) -> None:
    """小数の減算ができること"""
    assert calculate(left, right, "subtract") == expected
