import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.preview_pane import preview_pane
from app.components.glyph_editor import glyph_editor
from app.components.glyph_gallery import glyph_gallery
from app.components.export_dialog import export_dialog
from app.components.help_overlay import help_overlay
from app.states.font_state import FontState


def preview_page() -> rx.Component:
    return rx.el.div(
        help_overlay(),
        export_dialog(),
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.h1(
                                    "Preview & Refine",
                                    class_name="text-3xl font-bold text-gray-900 mb-2 font-['Lora']",
                                ),
                                rx.el.p(
                                    "Test your font and fine-tune individual characters.",
                                    class_name="text-lg text-gray-600 max-w-2xl",
                                ),
                            ),
                            rx.cond(
                                FontState.generation_complete,
                                rx.el.button(
                                    rx.icon("download", class_name="w-5 h-5 mr-2"),
                                    "Export Font",
                                    on_click=FontState.set_show_export_dialog(True),
                                    class_name="flex items-center px-6 py-2.5 bg-indigo-600 text-white font-bold rounded-full hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all hover:scale-105 whitespace-nowrap",
                                ),
                            ),
                            class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                        ),
                        class_name="mb-8",
                    ),
                    rx.cond(
                        FontState.generation_complete,
                        rx.el.div(
                            preview_pane(),
                            rx.el.div(
                                rx.el.div(
                                    glyph_editor(),
                                    class_name="col-span-1 lg:col-span-1",
                                ),
                                rx.el.div(
                                    glyph_gallery(),
                                    class_name="col-span-1 lg:col-span-2",
                                ),
                                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="w-12 h-12 text-yellow-500 mb-4",
                            ),
                            rx.el.h3(
                                "Font Not Generated Yet",
                                class_name="text-xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "Please upload samples and generate your font first.",
                                class_name="text-gray-500 mt-2",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "Go to Dashboard",
                                    class_name="mt-6 px-6 py-2 bg-indigo-600 text-white rounded-full font-medium hover:bg-indigo-700",
                                ),
                                href="/",
                            ),
                            class_name="flex flex-col items-center justify-center p-12 bg-white rounded-3xl border border-gray-100",
                        ),
                    ),
                    class_name="max-w-6xl mx-auto w-full",
                ),
                class_name="p-8 flex-1 overflow-y-auto",
            ),
            class_name="flex-1 ml-0 md:ml-72 flex flex-col min-h-screen bg-slate-50 font-['Lora']",
        ),
        class_name="flex min-h-screen bg-slate-50 font-['Lora']",
    )