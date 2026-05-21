from nicegui import ui

from training.calculator import OPERATIONS, calculate

DEFAULT_OPERATION_KEY = "add"
BUTTON_CLASS = "h-14 rounded-lg text-xl font-semibold"
NUMBER_BUTTON_CLASS = f"{BUTTON_CLASS} bg-slate-700 text-white hover:bg-slate-600"
ACTION_BUTTON_CLASS = f"{BUTTON_CLASS} bg-slate-500 text-white hover:bg-slate-400"
OPERATOR_BUTTON_CLASS = f"{BUTTON_CLASS} bg-amber-500 text-white hover:bg-amber-400"


def format_number(value: float) -> str:
    return f"{value:g}"


def create_app() -> None:
    ui.page_title("足し算電卓")

    with (
        ui.column().classes("w-full min-h-screen items-center justify-center bg-zinc-200 p-4"),
        ui.card().classes("w-full max-w-sm gap-3 rounded-lg bg-zinc-950 p-4 shadow-xl"),
    ):
        operation = OPERATIONS[DEFAULT_OPERATION_KEY]
        state: dict[str, float | str | None] = {
            "left": None,
            "operator": None,
            "display": "0",
        }

        expression_label = ui.label("").classes("h-5 w-full text-right text-sm text-zinc-400")
        display_label = ui.label("0").classes(
            "w-full overflow-hidden rounded-lg bg-zinc-900 px-4 py-5 text-right text-5xl "
            "font-light text-white"
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

        with ui.grid(columns=4).classes("w-full gap-2"):
            ui.button("C", on_click=clear).classes(f"{ACTION_BUTTON_CLASS} col-span-3")
            ui.button(operation.symbol, on_click=choose_operation).classes(OPERATOR_BUTTON_CLASS)

            for digit in ("7", "8", "9"):
                ui.button(digit, on_click=lambda value=digit: append_digit(value)).classes(
                    NUMBER_BUTTON_CLASS
                )
            ui.button("=", on_click=resolve).classes(f"{OPERATOR_BUTTON_CLASS} row-span-4 h-full")

            for digit in ("4", "5", "6", "1", "2", "3"):
                ui.button(digit, on_click=lambda value=digit: append_digit(value)).classes(
                    NUMBER_BUTTON_CLASS
                )
            ui.button("0", on_click=lambda: append_digit("0")).classes(
                f"{NUMBER_BUTTON_CLASS} col-span-2"
            )
            ui.button(".", on_click=append_decimal).classes(NUMBER_BUTTON_CLASS)


create_app()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="足し算電卓", reload=False)
