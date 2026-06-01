import os
from typing import Protocol

from nicegui import ui

from training.calculator import OPERATIONS, CalculationOverflowError, DivisionByZeroError, calculate

DEFAULT_OPERATION_KEY = "add"
MAX_INTEGER_DIGITS = 6
MAX_FRACTIONAL_DIGITS = 4
BUTTON_CLASS = "h-14 w-full rounded-md text-xl font-semibold"
NUMBER_BUTTON_COLOR = "blue"
ACTION_BUTTON_COLOR = "grey-4"
CLEAR_BUTTON_COLOR = "blue"
OPERATOR_BUTTON_COLOR = "blue"

type CalculatorState = dict[str, float | str | None]


class TextLabel(Protocol):
    def set_text(self, text: str) -> object: ...


def format_number(value: float) -> str:
    return f"{value:g}"


def format_expression(left: float, operator: str, right: str | None = None) -> str:
    expression = f"{format_number(left)} {OPERATIONS[operator].symbol}"
    if right is None:
        return expression

    return f"{expression} {right}"


def append_digit(display: str, digit: str) -> str:
    """数字ボタン押下後の表示値を返す。"""
    if display == "0":
        return digit

    next_display = f"{display}{digit}"
    integer_part, _, fractional_part = next_display.lstrip("-").partition(".")
    if len(integer_part) > MAX_INTEGER_DIGITS:
        return display
    if len(fractional_part) > MAX_FRACTIONAL_DIGITS:
        return display

    return next_display


def append_decimal(display: str) -> str:
    """小数点ボタン押下後の表示値を返す。"""
    if "." in display:
        return display

    return f"{display}."


def toggle_sign(display: str) -> str:
    """符号反転ボタン押下後の表示値を返す。"""
    if display == "0":
        return display
    if display.startswith("-"):
        return display[1:]

    return f"-{display}"


def select_operation(
    left: float | None,
    operator: str | None,
    display: str,
    operation_key: str,
) -> tuple[float | None, str | None, str]:
    """演算子ボタン押下後の電卓状態を返す。"""
    if operator is not None and display == "0":
        return left, operation_key, display

    return float(display), operation_key, "0"


def resolve_operation(
    left: float | None,
    operator: str | None,
    display: str,
) -> tuple[float | None, str | None, str]:
    """イコールボタン押下後の電卓状態を返す。"""
    next_left, next_operator, next_display, _expression = resolve_operation_with_expression(
        left,
        operator,
        display,
    )
    return next_left, next_operator, next_display


def resolve_operation_with_expression(
    left: float | None,
    operator: str | None,
    display: str,
) -> tuple[float | None, str | None, str, str]:
    """イコールボタン押下後の電卓状態と式表示値を返す。"""
    if left is None or operator is None:
        return left, operator, display, ""

    try:
        result = calculate(left, float(display), operator)
    except DivisionByZeroError:
        return None, None, "Error", ""
    except CalculationOverflowError:
        return None, None, "Overflow", ""

    return None, None, format_number(result), format_expression(left, operator, display)


def resolve_percentage_operation(
    left: float | None,
    operator: str | None,
    display: str,
) -> tuple[float | None, str | None, str]:
    """パーセントボタン押下後の電卓状態を返す。"""
    if left is None or operator is None:
        return clear_state()

    percentage_value = float(display) / 100
    return resolve_operation(left, operator, format_number(percentage_value))


def clear_state() -> tuple[None, None, str]:
    """クリアボタン押下後の電卓状態を返す。"""
    return None, None, "0"


def clear_entry(
    left: float | None,
    operator: str | None,
) -> tuple[float | None, str | None, str]:
    """入力クリアボタン押下後の電卓状態を返す。"""
    return left, operator, "0"


def initial_state() -> CalculatorState:
    """ページ読み込み直後の電卓状態を返す。"""
    return {"left": None, "operator": None, "display": "0"}


def render_state(
    display_label: TextLabel,
    expression_label: TextLabel,
    state: CalculatorState,
) -> None:
    """電卓状態を表示ラベルに反映する。"""
    display_label.set_text(str(state["display"]))
    expression = state.get("expression")
    if isinstance(expression, str) and expression:
        expression_label.set_text(expression)
        return

    left = state["left"]
    operator = state["operator"]
    expression_label.set_text(
        format_expression(left, operator)
        if isinstance(left, float) and isinstance(operator, str)
        else ""
    )


def create_app() -> None:
    ui.page_title("電卓Webアプリ")

    with (
        ui.column().classes("w-full min-h-screen items-center justify-center bg-zinc-50 p-4"),
        ui.card().classes(
            "w-full max-w-md gap-4 rounded-lg border border-zinc-200 bg-zinc-200 p-5 "
            "shadow-2xl shadow-zinc-200"
        ),
    ):
        state = initial_state()

        with ui.row().classes("w-full items-center justify-between"):
            ui.label("電卓Webアプリ").classes("text-sm font-semibold text-zinc-500")
            expression_label = ui.label("").classes("h-5 text-right text-sm text-zinc-500")

        display_label = ui.label("0").classes(
            "w-full overflow-hidden rounded-lg border border-lime-950 bg-lime-200 px-5 py-6 "
            "text-right text-5xl font-mono font-semibold tracking-wider text-lime-950 "
            "shadow-inner"
        )

        def render() -> None:
            render_state(display_label, expression_label, state)

        def clear() -> None:
            left, operator, display = clear_state()
            state["left"] = left
            state["operator"] = operator
            state["display"] = display
            state["expression"] = ""
            render()

        def clear_current_entry() -> None:
            left, operator, display = clear_entry(
                state["left"] if isinstance(state["left"], float) else None,
                state["operator"] if isinstance(state["operator"], str) else None,
            )
            state["left"] = left
            state["operator"] = operator
            state["display"] = display
            state["expression"] = ""
            render()

        def press_digit(digit: str) -> None:
            display = str(state["display"])
            state["display"] = append_digit(display, digit)
            if not isinstance(state["operator"], str):
                state["expression"] = ""
            render()

        def press_decimal() -> None:
            display = str(state["display"])
            state["display"] = append_decimal(display)
            render()

        def press_sign_toggle() -> None:
            display = str(state["display"])
            state["display"] = toggle_sign(display)
            render()

        def choose_operation(operation_key: str) -> None:
            left, operator, display = select_operation(
                state["left"] if isinstance(state["left"], float) else None,
                state["operator"] if isinstance(state["operator"], str) else None,
                str(state["display"]),
                operation_key,
            )
            state["left"] = left
            state["operator"] = operator
            state["display"] = display
            state["expression"] = ""
            render()

        def resolve() -> None:
            left, operator, display, expression = resolve_operation_with_expression(
                state["left"] if isinstance(state["left"], float) else None,
                state["operator"] if isinstance(state["operator"], str) else None,
                str(state["display"]),
            )
            state["left"] = left
            state["operator"] = operator
            state["display"] = display
            state["expression"] = expression
            render()

        def resolve_percentage() -> None:
            left, operator, display = resolve_percentage_operation(
                state["left"] if isinstance(state["left"], float) else None,
                state["operator"] if isinstance(state["operator"], str) else None,
                str(state["display"]),
            )
            state["left"] = left
            state["operator"] = operator
            state["display"] = display
            state["expression"] = ""
            render()

        buttons = [
            ("C", clear),
            ("CE", clear_current_entry),
            ("±", press_sign_toggle),
            ("%", resolve_percentage),
            (OPERATIONS["divide"].symbol, lambda: choose_operation("divide")),
            ("7", lambda: press_digit("7")),
            ("8", lambda: press_digit("8")),
            ("9", lambda: press_digit("9")),
            (OPERATIONS["multiply"].symbol, lambda: choose_operation("multiply")),
            (OPERATIONS["subtract"].symbol, lambda: choose_operation("subtract")),
            ("4", lambda: press_digit("4")),
            ("5", lambda: press_digit("5")),
            ("6", lambda: press_digit("6")),
            (".", press_decimal),
            (OPERATIONS["add"].symbol, lambda: choose_operation("add")),
            ("1", lambda: press_digit("1")),
            ("2", lambda: press_digit("2")),
            ("3", lambda: press_digit("3")),
            ("0", lambda: press_digit("0")),
            ("=", resolve),
        ]

        with ui.grid(columns=5).classes("w-full gap-2"):
            for label, handler in buttons:
                if label.isdigit() or label == ".":
                    button_color = NUMBER_BUTTON_COLOR
                elif label in {"C", "CE"}:
                    button_color = CLEAR_BUTTON_COLOR
                elif label in {operation.symbol for operation in OPERATIONS.values()} | {
                    "%",
                    "=",
                    "±",
                }:
                    button_color = OPERATOR_BUTTON_COLOR
                else:
                    button_color = ACTION_BUTTON_COLOR

                button = ui.button(label, on_click=handler, color=button_color).classes(
                    BUTTON_CLASS
                )
                if button_color == ACTION_BUTTON_COLOR:
                    button.props("text-color=black")


if __name__ in {"__main__", "__mp_main__"}:
    create_app()
    ui.run(title="電卓Webアプリ", reload=False, port=int(os.environ.get("PORT", "8080")))
