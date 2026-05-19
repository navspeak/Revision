import json
import re
import uuid
import sys
from pathlib import Path

def make_id():
    return uuid.uuid4().hex[:8]

def md_to_notebook(md_path: Path) -> dict:
    text = md_path.read_text()
    cells = []

    # Split on ```python ... ``` blocks
    parts = re.split(r'(```python\n.*?```)', text, flags=re.DOTALL)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if part.startswith('```python'):
            # Code cell — strip fences
            code = re.sub(r'^```python\n', '', part)
            code = re.sub(r'\n```$', '', code)
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "id": make_id(),
                "metadata": {},
                "outputs": [],
                "source": code
            })
        else:
            cells.append({
                "cell_type": "markdown",
                "id": make_id(),
                "metadata": {},
                "source": part
            })

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

md_dir = Path(__file__).parent

for md_file in sorted(md_dir.glob("[1-9]*.md")):
    nb = md_to_notebook(md_file)
    out = md_file.with_suffix('.ipynb')
    out.write_text(json.dumps(nb, indent=1))
    print(f"Created {out.name}  ({len(nb['cells'])} cells)")
