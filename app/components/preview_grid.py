import reflex as rx
from app.states.upload_state import UploadState
from app.components.styles import Elevation


def sample_card(filename: str) -> rx.Component:
    """A single card for a sample with image and label input."""
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=rx.get_upload_url(filename),
                class_name="w-full h-32 object-contain bg-gray-50 rounded-t-xl p-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("x", class_name="w-4 h-4 text-gray-400"),
                    on_click=lambda: UploadState.remove_file(filename),
                    class_name="absolute top-2 right-2 p-1 bg-white rounded-full shadow-sm hover:bg-gray-100 transition-colors opacity-0 group-hover:opacity-100",
                ),
                class_name="relative",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.label(
                "Character",
                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1",
            ),
            rx.el.input(
                placeholder="e.g. 'A'",
                on_change=lambda text: UploadState.update_label(filename, text),
                max_length=1,
                class_name="w-full px-3 py-2 border border-gray-200 rounded-lg text-center text-lg font-bold text-indigo-900 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all bg-gray-50 focus:bg-white",
                default_value=UploadState.labels[filename],
            ),
            class_name="p-4 border-t border-gray-100",
        ),
        class_name=f"group relative bg-white rounded-xl {Elevation.LEVEL_1} hover:{Elevation.LEVEL_3} transition-all duration-300",
    )


def preview_grid() -> rx.Component:
    return rx.el.div(
        rx.cond(
            UploadState.has_files,
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Label Your Samples",
                        class_name="text-lg font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        f"{UploadState.file_count} samples uploaded. Assign a character to each.",
                        class_name="text-gray-500 text-sm",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.foreach(UploadState.uploaded_files, sample_card),
                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6",
                ),
                class_name=f"p-8 bg-white rounded-3xl {Elevation.LEVEL_2}",
            ),
        )
    )