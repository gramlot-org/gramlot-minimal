"""Command-line interface."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from .errors import BuildError
from .html import build_html
from .project import Project
from .provider import DEFAULT_PROVIDER, compile_project, load_provider

def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="gramlot-standalone")
    result.add_argument("--version", action="version", version="%(prog)s 0.0.0.dev0")
    commands = result.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="Build one offline HTML file")
    build.add_argument("source", help="Project directory containing pages/")
    build.add_argument("-o", "--output", required=True, help="Output .html path")
    build.add_argument("--provider", default=DEFAULT_PROVIDER, metavar="MODULE:CALLABLE",
                       help=argparse.SUPPRESS)
    build.add_argument("--build-info", help="Optional JSON build receipt path")
    return result

def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                         prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise

def run_build(args: argparse.Namespace) -> dict:
    project = Project.load(args.source)
    output = Path(args.output).expanduser().resolve()
    if output.suffix.lower() not in {".html", ".htm"}:
        raise BuildError("Output must use an .html or .htm extension")
    receipt_path = Path(args.build_info).expanduser().resolve() if args.build_info else None
    if receipt_path == output:
        raise BuildError("HTML output and build-info receipt must use different paths")
    compiled = compile_project(project, load_provider(args.provider))
    artifact, info = build_html(project, compiled)
    receipt = json.dumps(info, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n"
    _atomic_write(output, artifact)
    if receipt_path is not None:
        _atomic_write(receipt_path, receipt)
    return info

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        info = run_build(args)
    except (BuildError, OSError) as error:
        print(f"gramlot-standalone: error: {error}", file=sys.stderr)
        return 2
    print(f"Built {args.output}: {info['bytes']} bytes, {len(info['pages'])} page(s), sha256 {info['sha256']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
