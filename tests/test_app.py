import pytest

from training.app import append_digit


@pytest.mark.parametrize("digit", ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
def test_tv_001_number_button_displays_digit_from_initial_zero(digit: str) -> None:
    assert append_digit("0", digit) == digit
