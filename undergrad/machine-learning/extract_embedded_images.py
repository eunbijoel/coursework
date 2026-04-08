"""
Extract markdown-embedded data:image/*;base64,... into ./images/ and rewrite links.

Run from this folder (PowerShell):
  python .\\extract_embedded_images.py

Fixes huge one-line JSON notebooks: after running, open the .ipynb in Cursor's
Notebook editor — cells stay readable; figures load from images/*.png.
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent / "Gradient Descent.ipynb"
IMG_DIR = Path(__file__).resolve().parent / "images"

# One match per data URL (non-greedy would be wrong; base64 is single token)
IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(data:image/(png|jpeg|jpg);base64,([A-Za-z0-9+/=]+)\)"
)


def _source_as_str(source: str | list[str]) -> str:
    if isinstance(source, str):
        return source
    return "".join(source)


def _set_source(cell: dict, text: str) -> None:
    if not text.endswith("\n"):
        text = text + "\n"
    cell["source"] = [text]


def main() -> None:
    if not NOTEBOOK.is_file():
        raise SystemExit(f"Missing: {NOTEBOOK}")

    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    img_count = 0

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        text = _source_as_str(cell.get("source", []))
        if "data:image/" not in text or "base64," not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            nonlocal img_count
            alt, ext, b64 = m.group(1), m.group(2), m.group(3)
            ext = "jpg" if ext == "jpeg" else ext
            img_count += 1
            fname = f"figure-{img_count}.{ext}"
            IMG_DIR.mkdir(parents=True, exist_ok=True)
            (IMG_DIR / fname).write_bytes(base64.b64decode(b64))
            return f"![{alt}](images/{fname})"

        new_text = IMG_RE.sub(repl, text)
        _set_source(cell, new_text)

    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Done. Extracted {img_count} image(s) -> {IMG_DIR}")
    print(f"Rewrote {NOTEBOOK.name} (indented JSON; inline base64 removed from markdown).")


if __name__ == "__main__":
    main()
