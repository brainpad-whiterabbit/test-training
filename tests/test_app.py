from time import perf_counter

import pytest

from training.app import (
    append_decimal,
    append_digit,
    clear_state,
    resolve_operation,
    select_operation,
    toggle_sign,
)


@pytest.mark.parametrize("digit", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
def test_number_button_displays_digit_from_initial_zero(digit: str) -> None:
    """数字ボタン押下時に入力欄へ数値を追加表示できること"""
    assert append_digit("0", digit) == digit


def test_number_buttons_display_multiple_digits() -> None:
    """複数桁の数値を連続入力できること"""
    assert append_digit(append_digit("0", "1"), "2") == "12"


def test_decimal_button_appends_decimal_point() -> None:
    """小数点を入力できること"""
    assert append_decimal("1") == "1."


def test_decimal_button_does_not_append_duplicate_decimal_point() -> None:
    """小数点を複数入力できないこと"""
    assert append_decimal("1.2") == "1.2"


def test_decimal_button_from_initial_zero_can_create_decimal_value() -> None:
    """.5 を正しく扱えること"""
    assert append_digit(append_decimal("0"), "5") == "0.5"


def test_sign_toggle_converts_positive_number_to_negative_number() -> None:
    """± 押下時に負数へ変換できること"""
    assert toggle_sign("5") == "-5"


def test_sign_toggle_converts_negative_number_to_positive_number() -> None:
    """± 再押下時に正数へ戻せること"""
    assert toggle_sign("-5") == "5"


def test_consecutive_operation_input_is_ignored() -> None:
    """演算子連続入力時に後続入力を無効化できること"""
    assert select_operation(1.0, "add", "0", "subtract") == (1.0, "add", "0")


def test_consecutive_operation_input_keeps_previous_input() -> None:
    """不正演算子入力時も直前入力を保持できること"""
    left, operator, _display = select_operation(1.0, "add", "0", "subtract")

    assert left == 1.0
    assert operator == "add"


def test_equals_button_displays_calculation_result() -> None:
    """= 押下時に計算結果を表示できること"""
    left, operator, display = resolve_operation(1.0, "add", "2")

    assert left is None
    assert operator is None
    assert display == "3"


def test_clear_button_resets_formula_result_and_operation_state() -> None:
    """C 押下時に入力中の計算式、計算結果、演算状態を初期化できること"""
    left, operator, display = clear_state()

    assert left is None
    assert operator is None
    assert display == "0"


def test_button_press_updates_display_within_one_second() -> None:
    """ボタン押下後1秒以内に画面更新されること"""
    start = perf_counter()
    display = append_digit("0", "1")
    elapsed_seconds = perf_counter() - start

    assert display == "1"
    assert elapsed_seconds < 1
