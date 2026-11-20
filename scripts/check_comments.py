from pathlib import Path
import subprocess
import sys


def comment_lines(source: str) -> list[int]:
    return [number for number, line in enumerate(source.splitlines(), 1) if "<!--" in line]


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    failures = [
        f"{path}:{number}"
        for path in tracked
        if path and Path(path).suffix in {".md", ".svg"}
        for number in comment_lines(Path(path).read_text())
    ]
    if failures:
        print("HTML/XML comments are forbidden:\n" + "\n".join(failures), file=sys.stderr)
        return 1
    print("Comment ratchet: zero HTML/XML comments in tracked Markdown and SVG files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
