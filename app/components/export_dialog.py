import reflex as rx
from app.states.font_state import FontState
from app.components.styles import Colors


def export_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Export Your Font",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Font Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. My Handwriting",
                            default_value=FontState.font_metadata["name"],
                            on_change=lambda v: FontState.update_metadata("name", v),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Author",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Your Name",
                            default_value=FontState.font_metadata["author"],
                            on_change=lambda v: FontState.update_metadata("author", v),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Version",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="1.0",
                            default_value=FontState.font_metadata["version"],
                            on_change=lambda v: FontState.update_metadata("version", v),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500",
                        ),
                        class_name="mb-6",
                    ),
                    class_name="space-y-4",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 mr-3",
                        )
                    ),
                    rx.el.button(
                        rx.cond(
                            FontState.is_exporting,
                            rx.el.span(
                                "Generating TTF...", class_name="flex items-center"
                            ),
                            rx.el.span(
                                rx.icon("download", class_name="w-4 h-4 mr-2"),
                                "Download TTF",
                                class_name="flex items-center",
                            ),
                        ),
                        on_click=FontState.export_font,
                        disabled=FontState.is_exporting,
                        class_name=f"px-6 py-2 text-sm font-medium text-white {Colors.PRIMARY_BG} rounded-lg {Colors.PRIMARY_HOVER} shadow-sm disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-2xl p-6 w-full max-w-md z-50 shadow-xl focus:outline-none",
            ),
        ),
        open=FontState.show_export_dialog,
        on_open_change=FontState.set_show_export_dialog,
    )