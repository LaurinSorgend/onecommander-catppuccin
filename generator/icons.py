"""Convert catppuccin/vscode-icons into One Commander file and folder icon packs."""
import re
import shutil
import subprocess
from pathlib import Path

import fitz
from PIL import Image

from palettes import PALETTES

HERE = Path(__file__).parent
SOURCE = HERE / ".cache" / "vscode-icons"
REPO_URL = "https://github.com/catppuccin/vscode-icons"
OUT = HERE.parent / "icons"
ENTRY = re.compile(r"^  '?([\w.-]+)'?: \{(.*?)^  \},", re.S | re.M)
STRING = re.compile(r"'([^']*)'")
ILLEGAL = re.compile(r'[<>:"/\\|?*,]')
NAME_LIMIT = 120


def fetch():
    """Shallow-clone the icon repo on first run, fast-forward it afterwards."""
    if SOURCE.exists():
        subprocess.run(["git", "-C", str(SOURCE), "pull", "-q", "--ff-only"], check=True)
    else:
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO_URL, str(SOURCE)], check=True)


def mapping(filename, field):
    """Icon basename -> list of values for one field (fileExtensions, folderNames...)."""
    text = (SOURCE / "src" / "defaults" / filename).read_text(encoding="utf-8")
    result = {}
    for icon, body in ENTRY.findall(text):
        block = re.search(field + r": \[(.*?)\]", body, re.S)
        if block:
            result[icon] = STRING.findall(block.group(1))
    return result


def file_associations():
    """Icon -> extensions. Dotfiles like .gitignore count as the extension 'gitignore'.

    Multi-part extensions (vert.glsl) are dropped: One Commander only sees the last part.
    """
    claimed, result = set(), {}
    extensions = mapping("fileIcons.ts", "fileExtensions")
    dotfiles = {icon: [n[1:] for n in names if n.count(".") == 1 and n.startswith(".")]
                for icon, names in mapping("fileIcons.ts", "fileNames").items()}
    for source in (extensions, dotfiles):
        for icon, names in source.items():
            usable = (n.lower() for n in names if "." not in n and not ILLEGAL.search(n))
            fresh = [n for n in dict.fromkeys(usable) if n not in claimed]
            claimed.update(fresh)
            if fresh:
                result.setdefault(icon, []).extend(fresh)
    return result


def chunks(names):
    """Split a name list so each comma-joined filename stays under the Windows limit."""
    group = []
    for name in names:
        if group and len(",".join(group + [name])) > NAME_LIMIT:
            yield group
            group = []
        group.append(name)
    if group:
        yield group


def render(svg, size):
    """Rasterize a 16x16-viewBox SVG to a transparent PNG pixmap of `size` pixels."""
    page = fitz.open("svg", svg.read_bytes())[0]
    scale = size / page.rect.width
    return page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=True)


def write_icon(svg, folder, stem, sizes):
    """Write one SVG as stem.png into folder at the first size, other sizes into subfolders."""
    for i, size in enumerate(sizes):
        target = folder if i == 0 else folder / str(size)
        target.mkdir(parents=True, exist_ok=True)
        render(svg, size).save(target / f"{stem}.png", output="png")


def file_pack(flavor, folder):
    """32px icons plus a 16/ subfolder, named by comma-joined extensions."""
    svgs = SOURCE / "icons" / flavor.lower()
    for icon, names in file_associations().items():
        svg = svgs / f"{icon}.svg"
        if svg.exists():
            for group in chunks(names):
                write_icon(svg, folder, ",".join(group), (32, 16))
    thumbnail(svgs, ["python", "typescript", "rust", "markdown", "json", "image", "zip"],
              (314, 46)).save(folder / "Thumbnail.png")


def folder_pack(flavor, folder):
    """One 32px PNG per folder name; '.png' is the fallback for unmatched folders."""
    svgs = SOURCE / "icons" / flavor.lower()
    folder.mkdir(parents=True, exist_ok=True)
    render(svgs / "_folder.svg", 32).save(folder / ".png", output="png")
    written = set()
    for icon, names in mapping("folderIcons.ts", "folderNames").items():
        svg = svgs / f"folder_{icon}.svg"
        fresh = {n.lower() for n in names if not ILLEGAL.search(n)} - written
        if not svg.exists() or not fresh:
            continue
        pixmap = render(svg, 32)
        for name in fresh:
            pixmap.save(folder / f"{name}.png", output="png")
        written |= fresh
    thumbnail(svgs, ["_folder", "folder_src", "folder_docs", "folder_images", "folder_git"],
              (211, 36)).save(folder / "Thumbnail.png")


def thumbnail(svgs, icons, size):
    """A row of sample icons, vertically centered, for One Commander's settings picker."""
    edge = size[1] - 10
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    for i, icon in enumerate(icons):
        pm = render(svgs / f"{icon}.svg", edge)
        tile = Image.frombytes("RGBA", (pm.width, pm.height), pm.samples)
        img.paste(tile, (5 + i * (edge + 6), 5), tile)
    return img


def main():
    fetch()
    for flavor in PALETTES:
        name = f"Catppuccin{flavor}"
        for kind, build in (("FileIcons", file_pack), ("FolderIcons", folder_pack)):
            folder = OUT / kind / name
            shutil.rmtree(folder, ignore_errors=True)
            build(flavor, folder)
            print("wrote", folder, sum(1 for _ in folder.rglob("*.png")), "png")


if __name__ == "__main__":
    main()
