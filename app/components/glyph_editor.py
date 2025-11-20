import reflex as rx
from app.states.font_state import FontState
from app.components.styles import Elevation, Colors


def editor_slider(
    label: str,
    value: rx.Var,
    min_val: float,
    max_val: float,
    step: float,
    param_name: str,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                label,
                class_name="text-xs font-semibold uppercase text-gray-500 tracking-wider",
            ),
            rx.el.span(value, class_name="text-xs font-mono text-indigo-600 font-bold"),
            class_name="flex justify-between mb-2",
        ),
        rx.el.input(
            type="range",
            min=min_val,
            max=max_val,
            step=step,
            default_value=value,
            value=value,
            on_change=lambda v: FontState.update_glyph_style(param_name, v).throttle(
                50
            ),
            class_name="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600",
            key=param_name,
        ),
        class_name="mb-6",
    )


def glyph_editor() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                f"Editing: '{FontState.selected_char}'",
                class_name="text-lg font-semibold text-gray-800 mb-6",
            ),
            rx.el.div(
                rx.el.svg(
                    rx.el.path(
                        d=FontState.generated_glyphs[FontState.selected_char],
                        fill="none",
                        stroke="currentColor",
                        stroke_width=FontState.editor_thickness,
                        stroke_linecap="round",
                        stroke_linejoin="round",
                        class_name="text-indigo-900 transition-all duration-200",
                    ),
                    rx.el.line(
                        x1="0",
                        y1="10",
                        x2="100",
                        y2="10",
                        stroke="#e5e7eb",
                        stroke_width="1",
                        stroke_dasharray="4",
                    ),
                    rx.el.line(
                        x1="0",
                        y1="50",
                        x2="100",
                        y2="50",
                        stroke="#e5e7eb",
                        stroke_width="1",
                        stroke_dasharray="4",
                    ),
                    rx.el.line(
                        x1="0",
                        y1="90",
                        x2="100",
                        y2="90",
                        stroke="#e5e7eb",
                        stroke_width="1",
                        stroke_dasharray="4",
                    ),
                    viewBox="0 0 100 100",
                    class_name="w-32 h-32 mx-auto",
                ),
                class_name="bg-gray-50 rounded-xl border border-gray-200 p-4 mb-8 flex justify-center items-center",
            ),
            editor_slider(
                "Thickness", FontState.editor_thickness, 1.0, 10.0, 0.5, "thickness"
            ),
            editor_slider(
                "Slant (Degrees)", FontState.editor_slant, -20.0, 20.0, 1.0, "slant"
            ),
            rx.el.button(
                rx.icon("rotate-ccw", class_name="w-4 h-4 mr-2"),
                "Reset to Default",
                on_click=FontState.reset_glyph,
                class_name="w-full flex items-center justify-center px-4 py-2 rounded-lg border border-gray-200 text-gray-600 text-sm font-medium hover:bg-gray-50 hover:text-gray-900 transition-colors",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=f"bg-white rounded-3xl {Elevation.LEVEL_2} p-6 h-full",
    )