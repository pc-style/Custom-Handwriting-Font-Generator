import reflex as rx
from app.states.font_state import FontState


def help_step(number: str, title: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            number,
            class_name="flex-shrink-0 w-8 h-8 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold text-sm mr-4",
        ),
        rx.el.div(
            rx.el.h4(title, class_name="font-semibold text-gray-900"),
            rx.el.p(desc, class_name="text-sm text-gray-600 mt-1"),
        ),
        class_name="flex items-start",
    )


def help_overlay() -> rx.Component:
    return rx.cond(
        FontState.show_help,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Welcome to GlyphGen!",
                        class_name="text-xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Follow these steps to create your custom handwriting font:",
                        class_name="text-gray-600 mb-6",
                    ),
                    rx.el.div(
                        help_step(
                            "1",
                            "Upload Samples",
                            "Go to the home page and upload 3-5 images of your handwriting.",
                        ),
                        help_step(
                            "2",
                            "Label & Generate",
                            "Assign a character to each upload (e.g. 'A', 'g') and click Generate.",
                        ),
                        help_step(
                            "3",
                            "Preview & Refine",
                            "Use the Preview page to test your font and adjust individual glyphs.",
                        ),
                        help_step(
                            "4",
                            "Export",
                            "Download your custom TTF file and install it on your computer!",
                        ),
                        class_name="space-y-4 mb-8",
                    ),
                    rx.el.button(
                        "Got it!",
                        on_click=FontState.toggle_help,
                        class_name="w-full py-3 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="w-5 h-5 text-gray-400"),
                        on_click=FontState.toggle_help,
                        class_name="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    class_name="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full relative mx-4",
                ),
                class_name="fixed inset-0 z-40 flex items-center justify-center bg-black/30 backdrop-blur-[2px] animate-in fade-in duration-200",
            )
        ),
    )