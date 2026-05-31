import os

from nicegui import ui

from training.calculator import OPERATIONS, calculate

DEFAULT_OPERATION_KEY = "add"
BUTTON_CLASS = "h-14 w-full rounded-md text-xl font-semibold"
NUMBER_BUTTON_CLASS = f"{BUTTON_CLASS} bg-slate-100 text-zinc-950 hover:bg-slate-200"
ACTION_BUTTON_CLASS = NUMBER_BUTTON_CLASS
OPERATOR_BUTTON_CLASS = NUMBER_BUTTON_CLASS
INACTIVE_BUTTON_CLASS = NUMBER_BUTTON_CLASS


def format_number(value: float) -> str:
    return f"{value:g}"


def append_digit(display: str, digit: str) -> str:
    """Return the display after pressing a digit button."""
    if display == "0":
        return digit

    return f"{display}{digit}"


def create_app() -> None:
    ui.page_title("電卓Webアプリ")

    with (
        ui.column().classes("w-full min-h-screen items-center justify-center bg-zinc-50 p-4"),
        ui.card().classes(
            "w-full max-w-md gap-4 rounded-lg border border-zinc-200 bg-zinc-200 p-5 "
            "shadow-2xl shadow-zinc-200"
        ),
    ):
        state: dict[str, float | str | None] = {
            "left": None,
            "operator": None,
            "display": "0",
        }

        with ui.row().classes("w-full items-center justify-between"):
            ui.label("電卓Webアプリ").classes("text-sm font-semibold text-zinc-500")
            expression_label = ui.label("").classes("h-5 text-right text-sm text-zinc-500")

        display_label = ui.label("0").classes(
            "w-full overflow-hidden rounded-lg border border-lime-950 bg-lime-200 px-5 py-6 "
            "text-right text-5xl font-mono font-semibold tracking-wider text-lime-950 "
            "shadow-inner"
        )

        def render() -> None:
            display_label.set_text(str(state["display"]))
            left = state["left"]
            operator = state["operator"]
            expression_label.set_text(
                f"{format_number(left)} {OPERATIONS[operator].symbol}"
                if isinstance(left, float) and isinstance(operator, str)
                else ""
            )

        def clear() -> None:
            state["left"] = None
            state["operator"] = None
            state["display"] = "0"
            render()

        def press_digit(digit: str) -> None:
            display = str(state["display"])
            state["display"] = append_digit(display, digit)
            render()

        def append_decimal() -> None:
            display = str(state["display"])
            if "." not in display:
                state["display"] = f"{display}."
            render()

        def choose_operation(operation_key: str) -> None:
            state["left"] = float(str(state["display"]))
            state["operator"] = operation_key
            state["display"] = "0"
            render()

        def resolve() -> None:
            left = state["left"]
            operator = state["operator"]
            if not isinstance(left, float) or not isinstance(operator, str):
                return

            right = float(str(state["display"]))
            state["display"] = format_number(calculate(left, right, operator))
            state["left"] = None
            state["operator"] = None
            render()

        buttons = [
            ("C", clear),
            ("CE", None),
            ("±", None),
            ("%", None),
            ("÷", None),
            ("7", lambda: press_digit("7")),
            ("8", lambda: press_digit("8")),
            ("9", lambda: press_digit("9")),
            ("x", None),
            (OPERATIONS["subtract"].symbol, lambda: choose_operation("subtract")),
            ("4", lambda: press_digit("4")),
            ("5", lambda: press_digit("5")),
            ("6", lambda: press_digit("6")),
            (".", append_decimal),
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
                    button_class = NUMBER_BUTTON_CLASS
                elif handler is None:
                    button_class = INACTIVE_BUTTON_CLASS
                elif label in {operation.symbol for operation in OPERATIONS.values()} | {"="}:
                    button_class = OPERATOR_BUTTON_CLASS
                else:
                    button_class = ACTION_BUTTON_CLASS

                ui.button(label, on_click=handler or (lambda: None)).classes(button_class)


if __name__ in {"__main__", "__mp_main__"}:
    create_app()
    ui.run(title="電卓Webアプリ", reload=False, port=int(os.environ.get("PORT", "8080")))
