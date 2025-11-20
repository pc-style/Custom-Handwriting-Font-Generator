import reflex as rx
from app.states.font_state import FontState
from app.states.upload_state import UploadState
from app.components.styles import Elevation, Colors


def generation_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Generation Studio", class_name="text-xl font-bold text-gray-900 mb-2"
            ),
            rx.el.p(
                "Create your custom font based on the analyzed style of your uploads.",
                class_name="text-gray-600 mb-6",
            ),
            rx.cond(
                FontState.is_generating,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            class_name="bg-indigo-600 h-2.5 rounded-full transition-all duration-300",
                            style={"width": f"{FontState.progress}%"},
                        ),
                        class_name="w-full bg-gray-200 rounded-full h-2.5 mb-2",
                    ),
                    rx.el.p(
                        f"Generating Glyphs... {FontState.progress}%",
                        class_name="text-sm font-medium text-indigo-600 text-center",
                    ),
                    class_name="w-full max-w-md mx-auto",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("wand-sparkles", class_name="w-5 h-5 mr-2"),
                        "Generate Font",
                        on_click=FontState.generate_font,
                        disabled=~UploadState.has_files,
                        class_name=f"flex items-center px-8 py-3 rounded-full {Colors.PRIMARY_BG} text-white font-bold {Colors.PRIMARY_HOVER} shadow-lg shadow-indigo-200 transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100",
                    ),
                    rx.cond(
                        ~UploadState.has_files,
                        rx.el.p(
                            "Upload at least one sample to start.",
                            class_name="text-xs text-red-500 mt-2 font-medium",
                        ),
                    ),
                    class_name="flex flex-col items-center",
                ),
            ),
            class_name="flex flex-col items-center justify-center p-8",
        ),
        rx.cond(
            FontState.generation_complete,
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Detected Thickness:", class_name="text-sm text-gray-500"
                    ),
                    rx.el.span(
                        f"{FontState.style_stats['thickness']}px",
                        class_name="font-mono font-bold text-gray-800",
                    ),
                    class_name="flex flex-col items-center p-4 bg-gray-50 rounded-xl",
                ),
                rx.el.div(
                    rx.el.span("Detected Slant:", class_name="text-sm text-gray-500"),
                    rx.el.span(
                        f"{FontState.style_stats['slant']}°",
                        class_name="font-mono font-bold text-gray-800",
                    ),
                    class_name="flex flex-col items-center p-4 bg-gray-50 rounded-xl",
                ),
                rx.el.div(
                    rx.el.span("Glyphs Generated:", class_name="text-sm text-gray-500"),
                    rx.el.span(
                        f"{FontState.generated_glyphs.length()}",
                        class_name="font-mono font-bold text-indigo-600",
                    ),
                    class_name="flex flex-col items-center p-4 bg-indigo-50 rounded-xl border border-indigo-100",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.button(
                            "Preview & Refine Font",
                            rx.icon("arrow-right", class_name="w-4 h-4 ml-2"),
                            class_name=f"flex items-center px-6 py-3 rounded-full {Colors.PRIMARY_BG} text-white font-bold {Colors.PRIMARY_HOVER} shadow-lg shadow-indigo-200 transition-all hover:scale-105 mt-8",
                        ),
                        href="/preview",
                    ),
                    class_name="col-span-3 flex justify-center w-full",
                ),
                class_name="grid grid-cols-3 gap-4 w-full max-w-2xl mt-8",
            ),
        ),
        class_name=f"bg-white rounded-3xl {Elevation.LEVEL_2} mt-8 overflow-hidden",
    )