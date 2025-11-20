import reflex as rx
import asyncio
import logging
from app.states.upload_state import UploadState
from app.utils.analyzer import analyze_image_style
from app.utils.generator import generate_char_path


class FontState(rx.State):
    generated_glyphs: dict[str, str] = {}
    style_stats: dict[str, float | int] = {
        "thickness": 2.0,
        "slant": 0.0,
        "baseline": 50,
    }
    char_styles: dict[str, dict] = {}
    preview_text: str = "The quick brown fox jumps over 123 fences."
    selected_char: str = "A"
    editor_thickness: float = 2.0
    editor_slant: float = 0.0
    editor_baseline: int = 50
    is_generating: bool = False
    progress: int = 0
    generation_complete: bool = False
    target_chars: list[str] = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "+",
        "-",
        "=",
        "<",
        ">",
        "/",
        "*",
        "∑",
        "∫",
        "α",
        "β",
        "π",
    ]
    LATEX_MAP: dict[str, str] = {
        "\\sum": "∑",
        "\\int": "∫",
        "\x07lpha": "α",
        "\x08eta": "β",
        "\\pi": "π",
        "\times": "*",
        "\\div": "/",
    }
    show_export_dialog: bool = False
    is_exporting: bool = False
    font_metadata: dict[str, str] = {
        "name": "My Handwriting",
        "author": "Me",
        "version": "1.0",
    }
    show_help: bool = True

    @rx.event
    def toggle_help(self):
        self.show_help = not self.show_help

    @rx.event
    def set_show_export_dialog(self, show: bool):
        self.show_export_dialog = show

    @rx.event
    def update_metadata(self, field: str, value: str):
        self.font_metadata[field] = value

    @rx.event
    async def export_font(self):
        """Generate and download the font file."""
        self.is_exporting = True
        yield
        try:
            from app.utils.font_export import generate_ttf_bytes

            ttf_data = generate_ttf_bytes(
                self.generated_glyphs, self.font_metadata, self.style_stats
            )
            if not ttf_data:
                yield rx.toast.error("Failed to generate font file.")
                return
            filename = f"{self.font_metadata['name'].replace(' ', '_')}.ttf"
            yield rx.download(data=ttf_data, filename=filename)
            yield rx.toast.success("Font downloaded successfully!")
            self.show_export_dialog = False
        except Exception as e:
            logging.exception(f"Export failed: {e}")
            yield rx.toast.error(f"Export failed: {str(e)}")
        finally:
            self.is_exporting = False

    @rx.var
    def preview_chars(self) -> list[str]:
        """Parse preview text to handle simple LaTeX commands and return list of chars."""
        text = self.preview_text
        for cmd, char in self.LATEX_MAP.items():
            text = text.replace(cmd, char)
        return list(text)

    @rx.event
    def set_preview_text(self, text: str):
        self.preview_text = text

    @rx.event
    def select_char(self, char: str):
        """Select a character for editing and load its styles."""
        if char not in self.generated_glyphs:
            return
        self.selected_char = char
        style = self.char_styles.get(char, self.style_stats)
        self.editor_thickness = float(
            style.get("thickness", self.style_stats["thickness"])
        )
        self.editor_slant = float(style.get("slant", self.style_stats["slant"]))
        self.editor_baseline = int(style.get("baseline", self.style_stats["baseline"]))

    @rx.event
    def update_glyph_style(self, param: str, value: float | int):
        """Update the style of the selected glyph immediately."""
        if param == "thickness":
            self.editor_thickness = float(value)
        elif param == "slant":
            self.editor_slant = float(value)
        elif param == "baseline":
            self.editor_baseline = int(value)
        current_style = {
            "thickness": self.editor_thickness,
            "slant": self.editor_slant,
            "baseline": self.editor_baseline,
        }
        self.char_styles[self.selected_char] = current_style
        new_path = generate_char_path(self.selected_char, current_style)
        self.generated_glyphs[self.selected_char] = new_path

    @rx.event
    def reset_glyph(self):
        """Reset selected glyph to global styles."""
        if self.selected_char in self.char_styles:
            del self.char_styles[self.selected_char]
        self.editor_thickness = self.style_stats["thickness"]
        self.editor_slant = self.style_stats["slant"]
        self.editor_baseline = self.style_stats["baseline"]
        new_path = generate_char_path(self.selected_char, self.style_stats)
        self.generated_glyphs[self.selected_char] = new_path

    @rx.event(background=True)
    async def generate_font(self):
        """Generate the full font set based on uploaded samples."""
        async with self:
            if self.is_generating:
                return
            self.is_generating = True
            self.progress = 0
            self.generation_complete = False
            self.generated_glyphs = {}
            upload_state = await self.get_state(UploadState)
            files = upload_state.uploaded_files
            if not files:
                self.style_stats = {"thickness": 4.0, "slant": 0.0, "baseline": 50}
            else:
                upload_dir = rx.get_upload_dir()
                thicknesses = []
                slants = []
                count = 0
                for filename in files[:3]:
                    file_path = upload_dir / filename
                    if file_path.exists():
                        stats = analyze_image_style(file_path)
                        thicknesses.append(stats["thickness"])
                        slants.append(stats["slant"])
                        count += 1
                if count > 0:
                    self.style_stats = {
                        "thickness": sum(thicknesses) / count,
                        "slant": sum(slants) / count,
                        "baseline": 50,
                    }
        total_chars = len(self.target_chars)
        batch_size = 5
        for i in range(0, total_chars, batch_size):
            batch = self.target_chars[i : i + batch_size]
            async with self:
                for char in batch:
                    svg_path = generate_char_path(char, self.style_stats)
                    self.generated_glyphs[char] = svg_path
                self.progress = int((i + len(batch)) / total_chars * 100)
            await asyncio.sleep(0.1)
        async with self:
            self.is_generating = False
            self.generation_complete = True
            yield rx.toast.success("Font generation complete!")