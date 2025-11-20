import reflex as rx
from app.states.upload_state import UploadState
from app.components.styles import Elevation, Colors

UPLOAD_ID = "handwriting_upload"


def upload_area() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "cloud-upload", class_name="w-12 h-12 text-indigo-400 mb-4"
                    ),
                    rx.el.h3(
                        "Drag & drop your handwriting samples",
                        class_name="text-lg font-medium text-gray-700 mb-1",
                    ),
                    rx.el.p(
                        "Supports PNG, JPG (Max 5MB per file)",
                        class_name="text-sm text-gray-500 mb-6",
                    ),
                    rx.el.button(
                        "Choose Files",
                        type="button",
                        class_name=f"px-6 py-2.5 rounded-full bg-indigo-50 text-indigo-700 font-medium hover:bg-indigo-100 transition-colors",
                    ),
                    class_name="flex flex-col items-center justify-center",
                ),
                class_name="w-full h-64 border-2 border-dashed border-indigo-100 rounded-2xl bg-indigo-50/30 flex items-center justify-center hover:bg-indigo-50/50 transition-colors cursor-pointer",
            ),
            id=UPLOAD_ID,
            accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
            multiple=True,
            max_files=10,
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Selected files:",
                    class_name="text-sm font-medium text-gray-700 mr-2",
                ),
                rx.foreach(
                    rx.selected_files(UPLOAD_ID),
                    lambda file: rx.el.span(
                        file,
                        class_name="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full mr-2 mb-2",
                    ),
                ),
                class_name="flex flex-wrap items-center mt-4",
            ),
            rx.cond(
                rx.selected_files(UPLOAD_ID).length() > 0,
                rx.el.div(
                    rx.el.button(
                        "Clear",
                        on_click=rx.clear_selected_files(UPLOAD_ID),
                        class_name="text-sm text-red-500 hover:text-red-700 mr-4 font-medium",
                    ),
                    rx.el.button(
                        rx.cond(
                            UploadState.is_uploading,
                            rx.el.span(
                                "Uploading...", class_name="flex items-center gap-2"
                            ),
                            "Upload Selected Samples",
                        ),
                        on_click=UploadState.handle_upload(
                            rx.upload_files(upload_id=UPLOAD_ID)
                        ),
                        disabled=UploadState.is_uploading,
                        class_name=f"px-6 py-2.5 rounded-full {Colors.PRIMARY_BG} text-white font-medium {Colors.PRIMARY_HOVER} shadow-lg shadow-indigo-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed",
                    ),
                    class_name="flex items-center justify-end mt-4",
                ),
            ),
        ),
        class_name=f"p-8 bg-white rounded-3xl {Elevation.LEVEL_2} mb-8",
    )