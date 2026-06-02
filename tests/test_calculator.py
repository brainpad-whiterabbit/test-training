import pytest

from training.app import append_digit, resolve_operation_with_expression
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


# ==============================================================================
# 1. F-14 (計算結果桁数制限) & F-12 (エラー表示) のテスト
# ==============================================================================
@pytest.mark.parametrize(
    ("left", "operator", "display", "expected_internal_msg"),
    [
        # F-14: 計算結果桁数制限
        (999999.0, "add", "1", "CalculationOverflowError"),
        (999999.0, "multiply", "2", "CalculationOverflowError"),
        (999999.0, "divide", "0.1", "CalculationOverflowError"),
        # F-12: エラー表示 (0除算)
        (5.0, "divide", "0", "DivisionByZeroError"),
    ],
    ids=[
        "overflow-addition",
        "overflow-multiplication",
        "overflow-division",
        "zero-division-error",
    ],
)
def test_resolve_operation_messages(
    left: float, operator: str, display: str, expected_internal_msg: str
) -> None:
    """計算実行時に、内部ロジック関数からエラー識別用の文字列が正しく返ること"""
    # Act: 4つの戻り値を受け取る形に修正
    _, _, result_display, _ = resolve_operation_with_expression(left, operator, display)

    # Assert: 戻り値のdisplay部分に入っている識別文字列を検証
    assert result_display == expected_internal_msg


# ==============================================================================
# 2. F-13 (表示桁数制限) のテスト
# ==============================================================================
@pytest.mark.parametrize(
    ("current_display", "input_digit", "expected_display"),
    [
        ("12345", "6", "123456"),
        ("123456", "7", "123456"),
        ("0.123", "4", "0.1234"),
        ("0.1234", "5", "0.1234"),
        ("123456.123", "4", "123456.1234"),
        ("123456.1234", "5", "123456.1234"),
    ],
    ids=[
        "integer-6-digits-ok",
        "integer-7-digits-ignored",
        "decimal-4-digits-ok",
        "decimal-5-digits-ignored",
        "total-10-digits-ok",
        "total-11-digits-ignored",
    ],
)
def test_display_length_limits(
    current_display: str, input_digit: str, expected_display: str
) -> None:
    """文字が入力された際、桁数制限の上限を超えた入力は無視されること"""
    result_display = append_digit(current_display, input_digit)
    assert result_display == expected_display
