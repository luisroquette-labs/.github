from pathlib import Path
import subprocess
import sys
from xml.parsers import expat


def comment_lines(source: str, suffix: str) -> list[int]:
    if suffix.lower() == ".svg":
        lines = []
        parser = expat.ParserCreate()
        parser.CommentHandler = lambda _: lines.append(parser.CurrentLineNumber)
        parser.Parse(source)
        return lines

    lines = []
    fence = ""
    for number, line in enumerate(source.splitlines(), 1):
        stripped = line.lstrip(" ")
        if len(line) - len(stripped) >= 4:
            continue
        marker = stripped[:1]
        if marker in {"`", "~"}:
            length = len(stripped) - len(stripped.lstrip(marker))
            if length >= 3 and (not fence or marker == fence[0] and length >= len(fence)):
                fence = "" if fence else marker * length
                continue
        if fence:
            continue
        code = 0
        index = 0
        while index < len(line):
            if line[index] == "`":
                end = index + len(line[index:]) - len(line[index:].lstrip("`"))
                run = end - index
                if code == 0:
                    code = run
                elif code == run:
                    code = 0
                index = end
            elif code == 0 and line.startswith("<!--", index):
                lines.append(number)
                break
            else:
                index += 1
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
