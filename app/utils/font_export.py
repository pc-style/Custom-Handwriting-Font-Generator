import io
import math
import logging
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


def _parse_svg_path(d_str: str) -> list[list[tuple[float, float]]]:
    """
    Parses a simple SVG path string (M x y L x y ...) into a list of polylines.
    Returns list of lists of (x, y) tuples.
    """
    polylines = []
    current_line = []
    parts = d_str.split()
    i = 0
    while i < len(parts):
        cmd = parts[i]
        if cmd == "M":
            if current_line:
                polylines.append(current_line)
            x = float(parts[i + 1])
            y = float(parts[i + 2])
            current_line = [(x, y)]
            i += 3
        elif cmd == "L":
            x = float(parts[i + 1])
            y = float(parts[i + 2])
            current_line.append((x, y))
            i += 3
        else:
            i += 1
    if current_line:
        polylines.append(current_line)
    return polylines


def _expand_stroke(
    polyline: list[tuple[float, float]], thickness: float
) -> list[tuple[float, float]]:
    """
    Converts a single line stroke into a closed loop polygon to simulate thickness.
    Naive implementation: traces forward, then traces backward with an offset.
    Coordinates are assumed to be 0-100 range from SVG.
    """
    if len(polyline) < 2:
        return []
    SCALE = 10.0
    points = []
    for x, y in polyline:
        points.append((x * SCALE, (100 - y) * SCALE))
    offset = thickness * SCALE * 0.5
    outline = []
    for p in points:
        outline.append((p[0] + offset, p[1] - offset))
    for p in reversed(points):
        outline.append((p[0] - offset, p[1] + offset))
    return outline


def generate_ttf_bytes(
    glyphs: dict[str, str], metadata: dict, style_stats: dict
) -> bytes:
    """
    Generates a TTF font file from the provided glyph paths.
    """
    try:
        font_name = metadata.get("name", "MyHandwriting")
        author = metadata.get("author", "GlyphGen User")
        fb = FontBuilder(1024, isTTF=True)
        char_map = {ord(c): f"glyph_{i:04d}" for i, c in enumerate(glyphs.keys())}
        glyph_order = [".notdef"] + list(char_map.values())
        fb.setupGlyphOrder(glyph_order)
        fb.setupCharacterMap(char_map)
        tt_glyphs = {}
        pen = TTGlyphPen(None)
        pen.moveTo((100, 0))
        pen.lineTo((100, 800))
        pen.lineTo((600, 800))
        pen.lineTo((600, 0))
        pen.closePath()
        tt_glyphs[".notdef"] = pen.glyph()
        base_thickness = style_stats.get("thickness", 2.0)
        for char, path_d in glyphs.items():
            glyph_name = char_map[ord(char)]
            pen = TTGlyphPen(None)
            polylines = _parse_svg_path(path_d)
            for poly in polylines:
                outline = _expand_stroke(poly, base_thickness)
                if len(outline) >= 3:
                    pen.moveTo(outline[0])
                    for pt in outline[1:]:
                        pen.lineTo(pt)
                    pen.closePath()
            if not polylines:
                pen.moveTo((0, 0))
                pen.lineTo((10, 0))
                pen.lineTo((10, 10))
                pen.lineTo((0, 10))
                pen.closePath()
            tt_glyphs[glyph_name] = pen.glyph()
        fb.setupGlyf(tt_glyphs)
        version_str = metadata.get("version", "1.0")
        clean_name = "".join((c for c in font_name if c.isalnum()))
        if not clean_name:
            clean_name = "MyHandwriting"
        name_table = {
            "familyName": font_name,
            "styleName": "Regular",
            "uniqueFontIdentifier": f"{author}:{clean_name}:{version_str}",
            "fullName": font_name,
            "psName": f"{clean_name}-Regular",
            "version": f"Version {version_str}",
            "manufacturer": "GlyphGen",
            "designer": author,
        }
        fb.setupNameTable(name_table)
        metrics = {g: (600, 50) for g in glyph_order}
        fb.setupHorizontalMetrics(metrics)
        fb.setupOS2(
            sTypoAscender=800, usWinAscent=800, sTypoDescender=-200, usWinDescent=200
        )
        fb.setupPost()
        stream = io.BytesIO()
        fb.save(stream)
        return stream.getvalue()
    except Exception as e:
        logging.exception(f"Error generating font: {e}")
        return b""