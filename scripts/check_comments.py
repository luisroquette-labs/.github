from pathlib import Path
import subprocess
import sys
from xml.parsers import expat
from markdown_it import MarkdownIt


def comment_lines(source: str, suffix: str) -> list[int]:
    if suffix.lower() == ".svg":
        lines = []
        parser = expat.ParserCreate()
        parser.CommentHandler = lambda _: lines.append(parser.CurrentLineNumber)
        parser.Parse(source)
        return lines

    lines = []
    for token in MarkdownIt("commonmark", {"html": True}).parse(source):
        if token.type == "html_block" and "<!--" in token.content:
            lines.append(token.map[0] + 1)
        elif token.type == "inline":
            lines.extend(token.map[0] + 1 for child in token.children or [] if child.type == "html_inline" and "<!--" in child.content)
    return lines


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    failures = [
        f"{path}:{number}"
        for path in tracked
        if path and Path(path).suffix.lower() in {".md", ".svg"}
        for number in comment_lines(Path(path).read_text(), Path(path).suffix)
    ]
    if failures:
        print("HTML/XML comments are forbidden:\n" + "\n".join(failures), file=sys.stderr)
        return 1
    print("Comment ratchet: zero HTML/XML comments in tracked Markdown and SVG files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
