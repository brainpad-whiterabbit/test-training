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
    ],
    ids=[
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-plus-negative-decimal",
        "negative-decimal-plus-positive-decimal",
        "negative-decimal-plus-negative-decimal",
        "positive-decimal-plus-zero",
        "integer-plus-positive-decimal",
        "positive-decimal-plus-integer",
        "positive-decimal-plus-positive-decimal",
        "positive-decimal-plus-positive-decimal",
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
        (-1, -1, 0),
        (-1, 3, -4),
        (1, -3, 4),
        (5, 1, 4),
        (0, 1, -1),
        (-999999, -10, -999989),
        (999999, 10, 999989),
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
def test_subtract_cases(left: float, right: float, expected: float) -> None:
    """減算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "subtract") == expected



# ==============================================================================
# 乗算（掛け算）のテスト
# ==============================================================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-2, -3, 6),
        (-2, 3, -6),
        (2, -3, -6),
        (2, 3, 6),
        (999999, 0, 0),
    ],
    ids=[
        "negative-multiply-negative",
        "negative-multiply-positive",
        "positive-multiply-negative",
        "positive-multiply-positive",
        "includes-zero",
    ],
)
def test_multiplication_cases(left: float, right: float, expected: float) -> None:
    """乗算の代表的な入力値の組み合わせを計算できること"""
    # 正しい演算子名 "multiply" に戻しました
    assert calculate(left, right, "multiply") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected_exception"),
    [
        (999999, 2, CalculationOverflowError),
        (-999999, 2, CalculationOverflowError),
        (999999, 999999, CalculationOverflowError),
        (-999999, -999999, CalculationOverflowError),
    ],
    ids=[
        "over-maximum",
        "under-minimum",
        "maximum-multiply-maximum",
        "minimum-multiply-minimum",
    ],
)
def test_multiplication_overflow_cases(
    left: float, right: float, expected_exception: type[BaseException]
) -> None:
    """乗算で値の範囲を超えた場合にCalculationOverflowErrorが発生すること"""
    with pytest.raises(expected_exception):
        calculate(left, right, "multiply")


# ==============================================================================
# 除算（割り算）のテスト
# ==============================================================================
@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (-6, -2, 3),
        (-6, 2, -3),
        (6, -2, -3),
        (6, 2, 3),
        (3, 2, 1.5),
        (0, 5, 0),
        (999999, 1, 999999),
        (-999999, 1, -999999),
    ],
    ids=[
        "negative-divide-negative",
        "negative-divide-positive",
        "positive-divide-negative",
        "positive-divide-positive",
        "indivisible-float",
        "divide-zero",
        "includes-maximum",
        "includes-minimum",
    ],
)
def test_division_cases(left: float, right: float, expected: float) -> None:
    """除算の代表的な入力値の組み合わせを計算できること"""
    assert calculate(left, right, "divide") == expected


@pytest.mark.parametrize(
    ("left", "right", "expected_exception"),
    [
        (5, 0, DivisionByZeroError),
        (-999999, -0.5, CalculationOverflowError),
    ],
    ids=[
        "zero-division",
        "over-maximum-by-division",
    ],
)
def test_division_error_cases(
    left: float, right: float, expected_exception: type[BaseException]
) -> None:
    """除算で不正な計算が行われた場合に適切な独自例外が発生すること"""
    with pytest.raises(expected_exception):
        calculate(left, right, "divide")
