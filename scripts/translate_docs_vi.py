from __future__ import annotations

import re
from pathlib import Path

from deep_translator import GoogleTranslator


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs"
DST = ROOT / "docs_vi"
SKIP_DIRS = {SRC / "onboarding-vi"}


def should_skip(path: Path) -> bool:
    for skip in SKIP_DIRS:
        try:
            path.relative_to(skip)
            return True
        except ValueError:
            continue
    return False


def split_code_fences(text: str) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    chunks = re.split(r"(```[\s\S]*?```)", text)
    for chunk in chunks:
        if not chunk:
            continue
        if chunk.startswith("```") and chunk.endswith("```"):
            parts.append(("code", chunk))
        else:
            parts.append(("text", chunk))
    return parts


def translate_chunk(translator: GoogleTranslator, chunk: str) -> str:
    lines = chunk.splitlines(keepends=True)
    out: list[str] = []
    batch: list[str] = []
    max_chars = 3500
    current_len = 0

    def flush() -> None:
        nonlocal batch, current_len
        if not batch:
            return
        text = "".join(batch)
        try:
            translated = translator.translate(text)
        except Exception:
            translated = text
        out.append(translated)
        batch = []
        current_len = 0

    for line in lines:
        if re.match(r"^\s*([-*]|\d+\.)\s+`[^`]+`\s*$", line) or re.match(
            r"^\s*#+\s+`[^`]+`\s*$", line
        ):
            flush()
            out.append(line)
            continue
        if "http://" in line or "https://" in line:
            flush()
            out.append(line)
            continue
        if current_len + len(line) > max_chars:
            flush()
        batch.append(line)
        current_len += len(line)
    flush()
    return "".join(out)


def translate_markdown(content: str) -> str:
    translator = GoogleTranslator(source="en", target="vi")
    sections = split_code_fences(content)
    output: list[str] = []
    for kind, value in sections:
        if kind == "code":
            output.append(value)
        else:
            output.append(translate_chunk(translator, value))
    return "".join(output)


def main() -> None:
    files = sorted(SRC.rglob("*.md"))
    translated_count = 0
    for src_file in files:
        if should_skip(src_file):
            continue
        rel = src_file.relative_to(SRC)
        dst_file = DST / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        content = src_file.read_text(encoding="utf-8", errors="ignore")
        translated = translate_markdown(content)
        header = (
            "<!-- Auto-translated from docs/ by script. Please review technical terms. -->\n\n"
        )
        dst_file.write_text(header + translated, encoding="utf-8")
        translated_count += 1
        print(f"Translated: {rel}", flush=True)
    print(f"Done. Total translated files: {translated_count}", flush=True)


if __name__ == "__main__":
    main()
