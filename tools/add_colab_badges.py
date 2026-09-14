#!/usr/bin/env python3
"""
add_colab_badges.py — put a one-click "Open in Colab" badge at the top of every
lab notebook, and fix the opening instructions to match.

Before the repository was public the notebooks told students to download the
file and use File > Upload notebook. Now that it is on GitHub, Colab can open a
notebook straight from the repository, which removes the step where a student
ends up editing a stale copy from their Downloads folder.

    python3 tools/add_colab_badges.py --repo BMGLab/BFB
    python3 tools/add_colab_badges.py --repo BMGLab/BFB --check   # report only

Re-running is safe: an existing badge is replaced rather than duplicated, so
this can be run again if the repository ever moves.
"""
import argparse
import json
import re
import sys
from pathlib import Path

BADGE_RE = re.compile(r"^\[!\[Open In Colab\].*?\)\s*\n+", re.M)
OLD_PROSE = re.compile(
    r"In Colab, upload this notebook through File > Upload notebook, then run cells "
    r"from top to bottom\.")
NEW_PROSE = ("Open it in Colab with the badge above, then **File > Save a copy in Drive** "
             "before you start so your work is kept. Run the cells from top to bottom.")


def badge(repo, name, branch):
    url = f"https://colab.research.google.com/github/{repo}/blob/{branch}/{name}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def as_lines(text):
    """Jupyter wants every source line to keep its newline, except the last."""
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/name, e.g. BMGLab/BFB")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--check", action="store_true", help="report without writing")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    changed = []
    for path in sorted(root.glob("*.ipynb")):
        nb = json.loads(path.read_text(encoding="utf-8"))
        if not nb.get("cells"):
            print(f"  skip (no cells): {path.name}")
            continue
        first = nb["cells"][0]
        if first.get("cell_type") != "markdown":
            nb["cells"].insert(0, {"cell_type": "markdown", "metadata": {}, "source": []})
            first = nb["cells"][0]

        text = "".join(first.get("source", []))
        text = BADGE_RE.sub("", text)                    # drop any previous badge
        text = OLD_PROSE.sub(NEW_PROSE, text)            # fix the stale instruction
        text = f"{badge(args.repo, path.name, args.branch)}\n\n{text.lstrip()}"
        first["source"] = as_lines(text)

        if args.check:
            print(f"  would update: {path.name}")
        else:
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
            print(f"  badged: {path.name}")
        changed.append(path.name)

    print(f"\n{len(changed)} notebook(s){' would be' if args.check else ''} updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
