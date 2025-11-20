import reflex as rx
from app.states.font_state import FontState
from app.components.styles import Elevation


def glyph_item(char: str) -> rx.Component:
    is_selected = FontState.selected_char == char
    return rx.el.button(
        rx.el.svg(
            rx.el.path(
                d=FontState.generated_glyphs[char],
                fill="none",
                stroke="currentColor",
                stroke_width=2,
                stroke_linecap="round",
                stroke_linejoin="round",
            ),
            viewBox="0 0 100 100",
            class_name=f"w-8 h-8 {rx.cond(is_selected, 'text-white', 'text-gray-700')}",
        ),
        on_click=lambda: FontState.select_char(char),
        class_name=rx.cond(
            is_selected,
            "p-2 rounded-lg bg-indigo-600 shadow-md transition-all transform scale-110",
            "p-2 rounded-lg bg-gray-50 hover:bg-gray-100 border border-gray-100 hover:border-gray-200 transition-all",
        ),
        title=f"Select '{char}'",
    )


def glyph_gallery() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Glyph Library", class_name="text-lg font-semibold text-gray-800"),
            rx.el.p(
                "Select a character to adjust its style.",
                class_name="text-sm text-gray-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.foreach(FontState.target_chars, glyph_item),
            class_name="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-10 gap-3 max-h-[400px] overflow-y-auto p-2",
        ),
        class_name=f"bg-white rounded-3xl {Elevation.LEVEL_2} p-6 h-full",
    )