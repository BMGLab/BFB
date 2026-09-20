#!/usr/bin/env python3
"""
audit_repo.py — read every file this repo would publish, and say what is in it.

Run this before the first push, and any time you add material:

    python3 tools/audit_repo.py

The pre-commit hook blocks by filename, which is deterministic but shallow.
This goes deeper: it extracts the actual text of PDFs, Office documents and
notebooks and looks for confidentiality banners, answer keys, student numbers
and e-mail addresses. PDF extraction needs pypdf; without it the PDF check is
skipped and the report says so rather than pretending the file was clean.

    pip install pypdf        # optional, but the PDF check needs it
"""
import json
import logging
import re
import sys
import warnings
import zipfile
from pathlib import Path

# pypdf logs a line per malformed cross-reference entry. PowerPoint's exporter
# produces these routinely and they are harmless, but a few hundred of them
# bury the actual findings — which is the whole point of the report.
warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

try:
    from pypdf import PdfReader
    HAVE_PDF = True
except ImportError:
    HAVE_PDF = False

# HARD: these appear only on instructor-only documents. Treat as a failure.
BANNER = re.compile(r"INSTRUCTOR ONLY|CONFIDENTIAL INSTRUCTOR|Assessment Keys", re.I)
# SOFT: worth a glance, but legitimate in student-facing prose — the handbook
# says answer keys are not published, and saying so is not a leak. Reported
# separately so a clean run stays clean and the report keeps its authority.
SOFT = re.compile(r"answer key|marking scheme|model answer|partial-credit|"
                  r"award \d+ marks?", re.I)
STUDENT_NO = re.compile(r"\b05\d{8}\b")
EMAIL = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.I)
SECRET = re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*\S{12,}", re.I)
SKIP_EMAIL = re.compile(r"example\.|noreply|@ege\.edu\.tr$", re.I)


def text_of(path):
    """Best-effort text, and whether extraction actually worked."""
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            if not HAVE_PDF:
                return "", False
            return "\n".join((p.extract_text() or "") for p in PdfReader(path).pages), True
        if suffix in (".docx", ".pptx", ".xlsx"):
            with zipfile.ZipFile(path) as z:
                raw = b"".join(z.read(n) for n in z.namelist() if n.endswith(".xml"))
            return re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "ignore")), True
        if suffix == ".ipynb":
            nb = json.loads(path.read_text(encoding="utf-8"))
            return "\n".join("".join(c.get("source", [])) for c in nb["cells"]), True
        if suffix in (".md", ".txt", ".py", ".csv", ".json", ".html", ".yml", ".yaml",
                      ".gs", ".js", ".ipynb", ".r", ".sh", ".applescript"):
            return path.read_text(encoding="utf-8", errors="ignore"), True
    except Exception as exc:
        return f"[unreadable: {exc}]", False
    return "", False


def main():
    root = Path(__file__).resolve().parent.parent
    # The guard tooling necessarily contains the very patterns it looks for.
    SELF = {"audit_repo.py", "pre-commit"}
    files = sorted(p for p in root.rglob("*")
                   if p.is_file()
                   and ".git" not in p.parts
                   and p.name not in SELF
                   and p.name != ".DS_Store")

    problems, soft, unchecked = [], [], []
    for path in files:
        rel = path.relative_to(root)
        body, ok = text_of(path)
        if not ok and path.suffix.lower() in (".pdf", ".docx", ".pptx", ".xlsx"):
            unchecked.append(rel)
            continue
        for label, pattern in (("confidentiality banner", BANNER),
                               ("student number", STUDENT_NO),
                               ("secret", SECRET)):
            hit = pattern.search(body)
            if hit:
                problems.append((rel, label, hit.group(0)[:60]))
        hit = SOFT.search(body)
        if hit:
            soft.append((rel, hit.group(0)[:60]))
        for m in EMAIL.finditer(body):
            if not SKIP_EMAIL.search(m.group(0)):
                problems.append((rel, "e-mail address", m.group(0)))

    print(f"audited {len(files)} files in {root.name}\n")
    if problems:
        print(f"{len(problems)} thing(s) to look at before publishing:\n")
        for rel, label, sample in problems:
            print(f"  {rel}\n      {label}: {sample!r}")
    else:
        print("  no confidentiality banners, student numbers, e-mails or secrets found")
    if soft:
        print(f"\n  {len(soft)} mention(s) of assessment wording — check the context, "
              f"these are usually fine:")
        for rel, sample in soft:
            print(f"      {rel}: {sample!r}")
    if unchecked:
        print(f"\n  {len(unchecked)} file(s) could not be read"
              f"{' (install pypdf for the PDF check)' if not HAVE_PDF else ''}:")
        for rel in unchecked[:12]:
            print(f"      {rel}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
