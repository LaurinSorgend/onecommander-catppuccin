"""Generate Catppuccin themes (all four flavors) for One Commander."""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from palettes import PALETTES, derived

HERE = Path(__file__).parent
THEMES = Path(r"C:\Users\Laurin\AppData\Local\OneCommander\Themes")
OUT = HERE.parent / "themes"
KEY = re.compile(r'x:Key="([^"]*)"')
COMMENT = re.compile(r"<!--.*?-->", re.S)


def render(flavor):
    """Fill the template for one flavor; fail on any unresolved placeholder."""
    roles = derived(flavor)
    text = (HERE / "template.xaml").read_text(encoding="utf-8")
    text = re.sub(r"@(\w+)@", lambda m: roles[m.group(1)], text)
    ET.fromstring(text)
    return text


def missing_keys(xaml):
    """Keys present in the bundled Dark theme but absent from the generated one."""
    dark = (THEMES / "Dark" / "Dark.xaml").read_text(encoding="utf-8")
    reference = set(KEY.findall(COMMENT.sub("", dark)))
    return sorted(reference - set(KEY.findall(xaml)))


def font(size):
    try:
        return ImageFont.truetype("segoeui.ttf", size)
    except OSError:
        return ImageFont.load_default()


def thumbnail(flavor):
    """Schematic 660x280 preview: sidebar, tabs, file list with one selected row."""
    d = derived(flavor)
    img = Image.new("RGB", (660, 280), d["crust"])
    draw = ImageDraw.Draw(img)
    draw.text((14, 8), f"Catppuccin {d['display']}", fill=d["text"], font=font(15))
    _sidebar(draw, d)
    _tabs(draw, d)
    _file_list(img, draw, d)
    return img


def _sidebar(draw, d):
    draw.rectangle((16, 44, 262, 270), fill=d["mantle"], outline=d["surface0"])
    draw.text((26, 52), "Drives", fill=d["subtext1"], font=font(18))
    for i, (name, used) in enumerate((("C:", 0.82), ("D:", 0.45))):
        y = 90 + i * 58
        draw.text((30, y), name, fill=d["text"], font=font(14))
        draw.text((170, y), f"{int(used * 100)}%", fill=d["text_secondary"], font=font(14))
        draw.rectangle((30, y + 24, 248, y + 30), fill=d["surface0"])
        draw.rectangle((30, y + 24, 30 + int(218 * used), y + 30), fill=d["blue"])


def _tabs(draw, d):
    draw.rectangle((290, 2, 470, 34), fill=d["base"])
    draw.text((302, 10), "Program Files", fill=d["text"], font=font(14))
    draw.rectangle((472, 2, 640, 34), fill=d["mantle"])
    draw.text((484, 10), "Windows", fill=d["text_secondary"], font=font(14))


def _file_list(img, draw, d):
    draw.rectangle((290, 34, 660, 280), fill=d["base"])
    draw.text((302, 42), "C:\\Program Files", fill=d["text"], font=font(20))
    rows = ["7-Zip", "Adobe", "Android", "Git", "Mozilla Firefox", "Windows Defender"]
    for i, name in enumerate(rows):
        y = 84 + i * 30
        if i % 2:
            _blend_rect(img, (290, y, 656, y + 28), d["zebra"], d["base"])
        if i == 1:
            _blend_rect(img, (290, y, 656, y + 28), d["select"], d["base"])
        draw = ImageDraw.Draw(img)
        draw.rectangle((302, y + 8, 316, y + 20), fill=d["yellow"])
        draw.text((326, y + 5), name, fill=d["text"], font=font(14))
        draw.text((600, y + 5), "DIR", fill=d["text_secondary"], font=font(13))
    ImageDraw.Draw(img).rectangle((656, 34, 658, 280), fill=d["blue"])


def _blend_rect(img, box, argb, under):
    alpha = int(argb[1:3], 16)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    color = tuple(int(argb[i:i + 2], 16) for i in (3, 5, 7)) + (alpha,)
    ImageDraw.Draw(overlay).rectangle(box, fill=color)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))


def main():
    for flavor in PALETTES:
        name = f"Catppuccin{flavor}"
        xaml = render(flavor)
        missing = missing_keys(xaml)
        if missing:
            sys.exit(f"{name}: missing keys {missing}")
        folder = OUT / name
        folder.mkdir(exist_ok=True)
        (folder / f"{name}.xaml").write_text(xaml, encoding="utf-8-sig")
        thumbnail(flavor).save(folder / "Thumbnail.png")
        print("wrote", folder)


if __name__ == "__main__":
    main()
