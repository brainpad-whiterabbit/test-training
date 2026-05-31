import pytest

from training.app import append_decimal, append_digit


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
