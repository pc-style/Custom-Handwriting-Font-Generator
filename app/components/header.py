import reflex as rx
from app.components.styles import Elevation
from app.states.font_state import FontState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("menu", class_name="w-6 h-6 text-gray-600"),
                    class_name="md:hidden mr-4 p-2 -ml-2 rounded-lg hover:bg-gray-100",
                ),
                rx.el.h2("Dashboard", class_name="text-xl font-semibold text-gray-800"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("circle-help", class_name="w-5 h-5 text-gray-600"),
                    on_click=FontState.toggle_help,
                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors mr-2",
                    title="Show Help",
                ),
                rx.el.button(
                    rx.icon("bell", class_name="w-5 h-5 text-gray-600"),
                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                ),
                rx.el.div(
                    rx.el.img(
                        src="/placeholder.svg",
                        class_name="w-8 h-8 rounded-full bg-indigo-100",
                    ),
                    class_name="ml-4",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=f"h-16 px-8 flex items-center bg-white/80 backdrop-blur-sm sticky top-0 z-10 border-b border-gray-100",
    )