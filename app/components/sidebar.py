import reflex as rx
from app.components.styles import Colors, Elevation
from app.states.font_state import FontState


def sidebar_item(icon: str, text: str, active: bool = False) -> rx.Component:
    return rx.el.div(
        rx.icon(
            icon,
            class_name=f"w-5 h-5 mr-3 {rx.cond(active, 'text-indigo-600', 'text-gray-500')}",
        ),
        rx.el.span(
            text,
            class_name=f"font-medium {rx.cond(active, 'text-indigo-900', 'text-gray-600')}",
        ),
        class_name=rx.cond(
            active,
            "flex items-center px-4 py-3 rounded-full bg-indigo-50 cursor-pointer transition-colors",
            "flex items-center px-4 py-3 rounded-full hover:bg-gray-100 cursor-pointer transition-colors",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("pen-tool", class_name="w-8 h-8 text-indigo-600 mr-2"),
                rx.el.h1(
                    "GlyphGen",
                    class_name="text-2xl font-bold text-gray-800 tracking-tight",
                ),
                class_name="flex items-center px-4 py-6 mb-6",
            ),
            rx.el.nav(
                rx.el.a(
                    sidebar_item("upload", "Upload Samples", active=True), href="/"
                ),
                rx.el.a(sidebar_item("type", "Preview & Refine"), href="/preview"),
                class_name="flex flex-col gap-2",
            ),
            rx.el.div(
                rx.el.div(class_name="h-px bg-gray-200 my-4"),
                sidebar_item("settings", "Settings"),
                rx.el.div(
                    sidebar_item("circle_help", "Help & Tutorials"),
                    on_click=FontState.toggle_help,
                ),
                class_name="mt-auto",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=f"w-72 h-screen bg-white border-r border-gray-100 p-4 hidden md:flex flex-col fixed left-0 top-0 {Elevation.LEVEL_1}",
    )