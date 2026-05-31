from time import perf_counter

import pytest

from training.app import (
    append_decimal,
    append_digit,
    clear_entry,
    clear_state,
    initial_state,
    render_state,
    resolve_operation,
    resolve_operation_with_expression,
    resolve_percentage_operation,
    select_operation,
    toggle_sign,
)


class FakeLabel:
    def __init__(self) -> None:
        self.text = ""

    def set_text(self, text: str) -> None:
        self.text = text


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


@pytest.mark.parametrize(
    ("display", "digit", "expected"),
    [
        ("99999", "9", "999999"),
        ("999999", "9", "999999"),
        ("-99999", "9", "-999999"),
        ("-999999", "9", "-999999"),
        ("1.999", "9", "1.9999"),
        ("1.9999", "9", "1.9999"),
        ("123456", "7", "123456"),
        ("0.1234", "5", "0.1234"),
    ],
    ids=[
        "integer-part-allows-six-digits",
        "integer-part-rejects-seventh-digit",
        "negative-integer-part-allows-six-digits",
        "negative-integer-part-rejects-seventh-digit",
        "fractional-part-allows-four-digits",
        "fractional-part-rejects-fifth-digit",
        "keeps-display-when-integer-limit-exceeded",
        "keeps-display-when-fractional-limit-exceeded",
    ],
)
def test_display_digit_limit_cases(display: str, digit: str, expected: str) -> None:
    """表示桁数制限に従って入力値を更新できること"""
    assert append_digit(display, digit) == expected


def test_sign_toggle_converts_positive_number_to_negative_number() -> None:
    """± 押下時に負数へ変換できること"""
    assert toggle_sign("5") == "-5"


def test_sign_toggle_converts_negative_number_to_positive_number() -> None:
    """± 再押下時に正数へ戻せること"""
    assert toggle_sign("-5") == "5"


def test_expression_display_shows_left_input_and_operator_during_second_input() -> None:
    """入力2の状態で入力1と演算子を式表示欄に表示できること"""
    state: dict[str, float | str | None] = {"left": 12.0, "operator": "add", "display": "3"}
    display_label = FakeLabel()
    expression_label = FakeLabel()

    render_state(display_label, expression_label, state)

    assert display_label.text == "3"
    assert expression_label.text == "12 +"


def test_expression_display_shows_full_expression_after_successful_calculation() -> None:
    """計算成功後に入力1と演算子と入力2を式表示欄に表示できること"""
    left, operator, display, expression = resolve_operation_with_expression(12.0, "add", "3")
    state: dict[str, float | str | None] = {
        "left": left,
        "operator": operator,
        "display": display,
        "expression": expression,
    }
    display_label = FakeLabel()
    expression_label = FakeLabel()

    render_state(display_label, expression_label, state)

    assert display_label.text == "15"
    assert expression_label.text == "12 + 3"


def test_consecutive_operation_input_overwrites_previous_operator() -> None:
    """演算子連続入力時に後続入力で演算子を上書きできること"""
    assert select_operation(1.0, "add", "0", "subtract") == (1.0, "subtract", "0")


def test_consecutive_operation_input_keeps_left_input_and_display() -> None:
    """演算子連続入力時も入力1と表示値を保持できること"""
    left, operator, _display = select_operation(1.0, "add", "0", "subtract")

    assert left == 1.0
    assert operator == "subtract"


def test_expression_display_reflects_overwritten_operator() -> None:
    """演算子連続入力後の式表示欄に上書き後の演算子を表示できること"""
    left, operator, display = select_operation(1.0, "add", "0", "subtract")
    state: dict[str, float | str | None] = {"left": left, "operator": operator, "display": display}
    display_label = FakeLabel()
    expression_label = FakeLabel()

    render_state(display_label, expression_label, state)

    assert display_label.text == "0"
    assert expression_label.text == "1 -"


def test_equals_button_displays_calculation_result() -> None:
    """= 押下時に計算結果を表示できること"""
    left, operator, display = resolve_operation(1.0, "add", "2")

    assert left is None
    assert operator is None
    assert display == "3"


def test_equals_button_can_resolve_multiplication() -> None:
    """x を使った計算結果を表示できること"""
    left, operator, display = resolve_operation(2.0, "multiply", "5")

    assert left is None
    assert operator is None
    assert display == "10"


def test_equals_button_can_resolve_division() -> None:
    """÷ を使った計算結果を表示できること"""
    left, operator, display = resolve_operation(10.0, "divide", "2")

    assert left is None
    assert operator is None
    assert display == "5"


def test_equals_button_displays_error_for_division_by_zero() -> None:
    """0除算時にErrorを表示できること"""
    left, operator, display = resolve_operation(10.0, "divide", "0")

    assert left is None
    assert operator is None
    assert display == "Error"


def test_clear_button_recovers_from_error() -> None:
    """Error後にC押下で正常操作へ復帰できること"""
    left, operator, display = resolve_operation(10.0, "divide", "0")
    assert display == "Error"

    left, operator, display = clear_state()

    assert left is None
    assert operator is None
    assert display == "0"
    assert append_digit(display, "1") == "1"


def test_clear_entry_recovers_from_error() -> None:
    """Error後にCE押下で正常操作へ復帰できること"""
    left, operator, display = resolve_operation(10.0, "divide", "0")
    assert display == "Error"

    left, operator, display = clear_entry(left, operator)

    assert left is None
    assert operator is None
    assert display == "0"
    assert append_digit(display, "1") == "1"


def test_equals_button_displays_overflow_for_out_of_range_result() -> None:
    """計算結果が表示桁数を超えた場合にOverflowを表示できること"""
    left, operator, display = resolve_operation(999999.0, "add", "1")

    assert left is None
    assert operator is None
    assert display == "Overflow"


@pytest.mark.parametrize(
    ("left", "operator", "display", "expected"),
    [
        (100.0, "add", "10", "110"),
        (100.0, "add", "0", "100"),
        (100.0, "add", "100", "200"),
        (100.0, "add", "150", "250"),
        (-100.0, "add", "10", "-110"),
        (100.0, "subtract", "10", "90"),
        (100.0, "subtract", "100", "0"),
        (100.0, "subtract", "150", "-50"),
        (-100.0, "subtract", "10", "-90"),
        (100.0, "multiply", "10", "10"),
        (200.0, "multiply", "12.5", "25"),
        (-100.0, "multiply", "10", "-10"),
        (100.0, "divide", "10", "1000"),
        (-100.0, "divide", "10", "-1000"),
        (1.0, "add", "33.333", "1.3333"),
    ],
    ids=[
        "adds-percentage-of-left",
        "adds-zero-percent-of-left",
        "adds-one-hundred-percent-of-left",
        "adds-more-than-one-hundred-percent-of-left",
        "adds-percentage-of-negative-left",
        "subtracts-percentage-of-left",
        "subtracts-one-hundred-percent-of-left",
        "subtracts-more-than-one-hundred-percent-of-left",
        "subtracts-percentage-of-negative-left",
        "multiplies-by-percentage",
        "multiplies-by-decimal-percentage",
        "multiplies-negative-left-by-percentage",
        "divides-by-percentage",
        "divides-negative-left-by-percentage",
        "rounds-percentage-result-to-four-decimal-places",
    ],
)
def test_percentage_button_resolves_operation_in_second_input_state(
    left: float,
    operator: str,
    display: str,
    expected: str,
) -> None:
    """入力2の状態で%押下時にパーセント計算ルールに従って計算できること"""
    next_left, next_operator, next_display = resolve_percentage_operation(left, operator, display)

    assert next_left is None
    assert next_operator is None
    assert next_display == expected


def test_percentage_button_displays_error_for_division_by_zero_percent() -> None:
    """入力1に対する0%で除算するとErrorを表示できること"""
    left, operator, display = resolve_percentage_operation(100.0, "divide", "0")

    assert left is None
    assert operator is None
    assert display == "Error"


@pytest.mark.parametrize(
    ("left", "operator", "display"),
    [
        (999999.0, "add", "1"),
        (-999999.0, "add", "1"),
    ],
    ids=["addition-exceeds-maximum", "negative-addition-exceeds-minimum"],
)
def test_percentage_button_displays_overflow_for_out_of_range_result(
    left: float,
    operator: str,
    display: str,
) -> None:
    """パーセント計算結果が表示桁数を超えた場合にOverflowを表示できること"""
    next_left, next_operator, next_display = resolve_percentage_operation(left, operator, display)

    assert next_left is None
    assert next_operator is None
    assert next_display == "Overflow"


@pytest.mark.parametrize(
    ("left", "operator", "display"),
    [
        (None, None, "0"),
        (None, None, "100"),
        (None, None, "110"),
    ],
    ids=["waiting-for-input", "first-input", "result-displayed"],
)
def test_percentage_button_clears_when_not_in_second_input_state(
    left: float | None,
    operator: str | None,
    display: str,
) -> None:
    """入力2以外の状態で%押下時にクリアできること"""
    next_left, next_operator, next_display = resolve_percentage_operation(left, operator, display)

    assert next_left is None
    assert next_operator is None
    assert next_display == "0"


def test_clear_button_resets_formula_result_and_operation_state() -> None:
    """C 押下時に入力中の計算式、計算結果、演算状態を初期化できること"""
    left, operator, display = clear_state()

    assert left is None
    assert operator is None
    assert display == "0"


def test_clear_entry_resets_display_and_keeps_operation_state() -> None:
    """CE 押下時に現在入力中の値だけを0にリセットできること"""
    left, operator, display = clear_entry(1.0, "add")

    assert left == 1.0
    assert operator == "add"
    assert display == "0"


def test_button_press_updates_display_within_one_second() -> None:
    """ボタン押下後1秒以内に画面更新されること"""
    state: dict[str, float | str | None] = {"left": None, "operator": None, "display": "0"}
    display_label = FakeLabel()
    expression_label = FakeLabel()

    start = perf_counter()
    state["display"] = append_digit(str(state["display"]), "1")
    render_state(display_label, expression_label, state)
    elapsed_seconds = perf_counter() - start

    assert display_label.text == "1"
    assert elapsed_seconds < 1


def test_rapid_button_presses_update_display_without_delay() -> None:
    """高速連打でも表示遅延しないこと"""
    state: dict[str, float | str | None] = {"left": None, "operator": None, "display": "0"}
    display_label = FakeLabel()
    expression_label = FakeLabel()

    start = perf_counter()
    for _ in range(100):
        state["display"] = append_digit(str(state["display"]), "1")
        render_state(display_label, expression_label, state)
    elapsed_seconds = perf_counter() - start

    assert display_label.text == "111111"
    assert elapsed_seconds < 1


def test_reload_starts_from_initial_state() -> None:
    """ページ再読み込み後に初期状態で開始できること"""
    assert initial_state() == {"left": None, "operator": None, "display": "0"}


def test_reload_does_not_keep_previous_operation_state() -> None:
    """リロード時に演算状態を保持しないこと"""
    previous_state = initial_state()
    previous_state["left"] = 1.0
    previous_state["operator"] = "add"
    previous_state["display"] = "2"

    reloaded_state = initial_state()

    assert reloaded_state["left"] is None
    assert reloaded_state["operator"] is None
    assert reloaded_state["display"] == "0"
