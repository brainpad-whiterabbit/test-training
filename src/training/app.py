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


def create_app() -> None:
    ui.page_title("電卓Webアプリ")

    with (
        ui.column().classes("w-full min-h-screen items-center justify-center bg-zinc-50 p-4"),
        ui.card().classes(
            "w-full max-w-md gap-4 rounded-lg border border-zinc-200 bg-zinc-200 p-5 "
            "shadow-2xl shadow-zinc-200"
        ),
    ):
        operation = OPERATIONS[DEFAULT_OPERATION_KEY]
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
                f"{format_number(left)} {operation.symbol}"
                if isinstance(left, float) and operator
                else ""
            )

        def clear() -> None:
            state["left"] = None
            state["operator"] = None
            state["display"] = "0"
            render()

        def append_digit(digit: str) -> None:
            display = str(state["display"])
            state["display"] = digit if display == "0" else f"{display}{digit}"
            render()

        def append_decimal() -> None:
            display = str(state["display"])
            if "." not in display:
                state["display"] = f"{display}."
            render()

        def choose_operation() -> None:
            state["left"] = float(str(state["display"]))
            state["operator"] = DEFAULT_OPERATION_KEY
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
            ("MC", None),
            ("MR", None),
            ("M-", None),
            ("M+", None),
            ("AC", None),
            ("CE", None),
            ("C", clear),
            ("±", None),
            ("%", None),
            ("÷", None),
            ("7", lambda: append_digit("7")),
            ("8", lambda: append_digit("8")),
            ("9", lambda: append_digit("9")),
            ("x", None),
            ("-", None),
            ("4", lambda: append_digit("4")),
            ("5", lambda: append_digit("5")),
            ("6", lambda: append_digit("6")),
            (operation.symbol, choose_operation),
            ("=", resolve),
            ("1", lambda: append_digit("1")),
            ("2", lambda: append_digit("2")),
            ("3", lambda: append_digit("3")),
            ("0", lambda: append_digit("0")),
            (".", append_decimal),
        ]

        with ui.grid(columns=5).classes("w-full gap-2"):
            for label, handler in buttons:
                if label.isdigit() or label == ".":
                    button_class = NUMBER_BUTTON_CLASS
                elif handler is None:
                    button_class = INACTIVE_BUTTON_CLASS
                elif label in {operation.symbol, "="}:
                    button_class = OPERATOR_BUTTON_CLASS
                else:
                    button_class = ACTION_BUTTON_CLASS

                ui.button(label, on_click=handler or (lambda: None)).classes(button_class)


create_app()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="電卓Webアプリ", reload=False, port=int(os.environ.get("PORT", "8080")))
