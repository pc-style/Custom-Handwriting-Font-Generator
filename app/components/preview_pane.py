import reflex as rx
from app.states.font_state import FontState
from app.components.styles import Elevation, Colors


def render_preview_char(char: str, index: int) -> rx.Component:
    char_width = 40
    spacing = 10
    x_pos = index * (char_width + spacing)
    return rx.el.g(
        rx.el.path(
            d=FontState.generated_glyphs[char],
            fill="none",
            stroke="currentColor",
            stroke_width=2,
            stroke_linecap="round",
            stroke_linejoin="round",
        ),
        transform=f"translate({x_pos}, 0)",
        class_name="text-indigo-900",
    )


def preview_pane() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Live Preview", class_name="text-lg font-semibold text-gray-800 mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.svg(
                        rx.foreach(
                            FontState.preview_chars,
                            lambda char, i: rx.cond(
                                FontState.generated_glyphs.contains(char),
                                render_preview_char(char, i),
                                rx.el.text(""),
                            ),
                        ),
                        viewBox=f"0 0 {FontState.preview_chars.length() * 50 + 100} 120",
                        class_name="w-full h-full",
                        preserveAspectRatio="xMidYMid meet",
                    ),
                    class_name="w-full h-32 bg-white rounded-xl border border-gray-200 mb-6 overflow-x-auto overflow-y-hidden",
                ),
                rx.el.div(
                    rx.el.input(
                        on_change=FontState.set_preview_text,
                        placeholder="Type here to preview font... (Try \\sum, \\alpha for math symbols)",
                        class_name="w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all text-gray-700 font-medium",
                        default_value=FontState.preview_text,
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Quick Samples:",
                            class_name="text-xs font-bold text-gray-400 mr-2",
                        ),
                        rx.el.button(
                            "Pangram",
                            on_click=lambda: FontState.set_preview_text(
                                "The quick brown fox jumps over the lazy dog."
                            ),
                            class_name="text-xs font-medium text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-full transition-colors",
                        ),
                        rx.el.button(
                            "Math",
                            on_click=lambda: FontState.set_preview_text(
                                "E = mc^2  |  \\alpha + \\beta = \\pi"
                            ),
                            class_name="text-xs font-medium text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-full transition-colors",
                        ),
                        rx.el.button(
                            "Calculus",
                            on_click=lambda: FontState.set_preview_text(
                                "\\int x^2 dx = \\frac{x^3}{3} + C"
                            ),
                            class_name="text-xs font-medium text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-full transition-colors",
                        ),
                        rx.el.button(
                            "Numbers",
                            on_click=lambda: FontState.set_preview_text(
                                "0123456789 +-*/= <>"
                            ),
                            class_name="text-xs font-medium text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-3 py-1 rounded-full transition-colors",
                        ),
                        class_name="flex flex-wrap items-center gap-2 mt-3",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="p-6",
        ),
        class_name=f"bg-white rounded-3xl {Elevation.LEVEL_2} mb-8 overflow-hidden",
    )