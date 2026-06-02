import pytest

from training.calculator import calculate

"""
加算のテスト
"""


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
        "includes-zero-addition",
        "includes-maximum-addition",
        "includes-minimum-addition",
    ],
)
def test_addition_cases(left: float, right: float, expected: float) -> None:
    """加算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "add") == expected


"""
減算のテスト
"""


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-1, -1, 0),
        (-1, 3, -4),
        (1, -3, 4),
        (5, 1, 4),
        (0, 1, -1),
        (999999, 10, 999989),
        (-999999, -10, -999989),
    ],
    ids=[
        "negative-subtraction-negative",
        "negative-subtraction-positive",
        "positive-subtraction-negative",
        "positive-subtraction-positive",
        "includes-zero-subtraction",
        "includes-maximum-subtration",
        "includes-minimum-subtraction",
    ],
)
def test_subtraction_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected


"""
乗算のテスト
"""


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (2, 3, 6),
        (-2, 3, -6),
        (-2, -3, 6),
        (-2, 0, 0),
    ],
    ids=[
        "positive-multiply-positive",
        "negative-multiply-positive",
        "negative-multiply-negative",
        "includes-zero-multiply",
    ],
)
def test_multiplication_cases(left: float, right: float, expected: float) -> None:
    """乗算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "multiply") == expected


"""
除算のテスト
"""


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [(6, 2, 3), (6, -3, -2), (-6, -3, 2), (0, 5, 0)],
    ids=[
        "positive-divide-positive",
        "positive-divide-negative",
        "negative-divide-negative",
        "includes-zero-integer",
    ],
)
def test_divide_cases(left: float, right: float, expected: float) -> None:
    """除算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "divide") == expected


"""
小数点数計算のテスト
"""


@pytest.mark.parametrize(
    ("left", "right", "operation_key", "expected"),
    [
        # 加算
        (1.5, 2.5, "add", 4.0),
        (1.5, -0.5, "add", 1.0),
        (-1.5, 0.5, "add", -1.0),
        (-1.5, -2.5, "add", -4.0),
        (1.5, 0, "add", 1.5),
        (1, 1.5, "add", 2.5),
        (1.5, 1, "add", 2.5),
        # 減算
        (2.5, 1.5, "subtract", 1),
        (2, 1.5, "subtract", 0.5),
        (1.5, 1, "subtract", 0.5),
    ],
    ids=[
        # 加算
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-plus-negative-decimal",
        "negative-decimal-plus-positive-decimal",
        "negative-decimal-plus-negative-decimal",
        "positive-decimal-plus-zero",
        "integer-plus-positive-decimal",
        "positive-decimal-plus-integer",
        # 減算
        "positive-decimal-subtract-decimal",
        "positive-integer-subtract-decimal",
        "positive-decimal-subtract-integer",
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
