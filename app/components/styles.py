import reflex as rx


class Elevation:
    LEVEL_0 = "shadow-none"
    LEVEL_1 = "shadow-sm border border-gray-100"
    LEVEL_2 = "shadow border border-gray-100"
    LEVEL_3 = "shadow-md border border-gray-100"
    LEVEL_4 = "shadow-lg border border-gray-100"
    LEVEL_5 = "shadow-xl border border-gray-100"


class Colors:
    PRIMARY = "indigo-600"
    PRIMARY_BG = "bg-indigo-600"
    PRIMARY_HOVER = "hover:bg-indigo-700"
    SECONDARY_TEXT = "text-gray-500"
    SURFACE = "bg-white"
    BACKGROUND = "bg-slate-50"


def card_style(elevation: str = Elevation.LEVEL_1) -> str:
    return f"{elevation} bg-white rounded-2xl"