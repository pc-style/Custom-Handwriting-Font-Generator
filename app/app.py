import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.upload_area import upload_area
from app.components.preview_grid import preview_grid
from app.components.generation_controls import generation_controls


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Create Your Custom Font",
                        class_name="text-3xl font-bold text-gray-900 mb-2 font-['Lora']",
                    ),
                    rx.el.p(
                        "Upload images of your handwriting to get started. We recommend 5-10 samples for best results.",
                        class_name="text-lg text-gray-600 mb-8 max-w-2xl",
                    ),
                    upload_area(),
                    preview_grid(),
                    generation_controls(),
                    class_name="max-w-6xl mx-auto",
                ),
                class_name="p-8 flex-1 overflow-y-auto",
            ),
            class_name="flex-1 ml-0 md:ml-72 flex flex-col min-h-screen bg-slate-50 font-['Lora']",
        ),
        class_name="flex min-h-screen bg-slate-50 font-['Lora']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.pages.preview import preview_page

app.add_page(index, route="/")
app.add_page(preview_page, route="/preview")