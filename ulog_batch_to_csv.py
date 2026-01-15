#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-convert .ulg files to CSV using the 'ulog2csv' tool from pyulog."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=".",
        help="Input folder to scan for .ulg files (default: current directory).",
    )
    parser.add_argument(
        "-o",
        "--output-base",
        default="csv",
        help="Base output directory (default: ./csv).",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only scan the input folder itself (no subfolders).",
    )
    parser.add_argument(
        "-m",
        "--messages",
        default=None,
        help="Comma-separated message names to export (same as ulog2csv -m).",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        default=None,
        help="CSV delimiter (same as ulog2csv -d).",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        action="store_true",
        help="Ignore string parsing exceptions (same as ulog2csv -i).",
    )
    parser.add_argument(
        "--time-s",
        type=float,
        default=None,
        help="Only convert data after this timestamp in seconds (same as ulog2csv -ts).",
    )
    parser.add_argument(
        "--time-e",
        type=float,
        default=None,
        help="Only convert data up to this timestamp in seconds (same as ulog2csv -te).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If an output directory for a log already exists, delete and recreate it.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without running ulog2csv.",
    )
    return parser.parse_args(argv)


def _iter_ulg_files(root: Path, recursive: bool) -> list[Path]:
    if recursive:
        files = list(root.rglob("*.ulg"))
    else:
        files = list(root.glob("*.ulg"))
    return sorted([p for p in files if p.is_file()])


def main(argv: list[str]) -> int:
    args = _parse_args(argv)

    ulog2csv = shutil.which("ulog2csv")
    if not ulog2csv:
        print("Error: 'ulog2csv' not found. Try: pip install --user pyulog", file=sys.stderr)
        return 2

    input_root = Path(args.input).expanduser().resolve()
    if not input_root.exists():
        print(f"Error: input path does not exist: {input_root}", file=sys.stderr)
        return 2

    output_base = Path(args.output_base).expanduser().resolve()
    recursive = not args.no_recursive

    if input_root.is_file():
        if input_root.suffix.lower() != ".ulg":
            print(f"Error: input file is not a .ulg: {input_root}", file=sys.stderr)
            return 2
        ulg_files = [input_root]
    else:
        ulg_files = _iter_ulg_files(input_root, recursive=recursive)
    if not ulg_files:
        print(f"No .ulg files found under: {input_root}")
        return 0

    failures: list[Path] = []
    for ulg_path in ulg_files:
        if input_root.is_file():
            rel_parent = Path(".")
        else:
            rel_parent = (
                Path(".")
                if ulg_path.parent == input_root
                else ulg_path.parent.relative_to(input_root)
            )
        out_dir = output_base / rel_parent / ulg_path.stem

        cmd: list[str] = [ulog2csv, str(ulg_path), "-o", str(out_dir)]
        if args.messages:
            cmd.extend(["-m", args.messages])
        if args.delimiter:
            cmd.extend(["-d", args.delimiter])
        if args.ignore:
            cmd.append("-i")
        if args.time_s is not None:
            cmd.extend(["-ts", str(args.time_s)])
        if args.time_e is not None:
            cmd.extend(["-te", str(args.time_e)])

        if args.overwrite and out_dir.exists():
            if args.dry_run:
                print(f"[dry-run] remove: {out_dir}")
            else:
                shutil.rmtree(out_dir)

        if args.dry_run:
            print("[dry-run]", " ".join(cmd))
            continue

        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            failures.append(ulg_path)
            print(f"Failed: {ulg_path}", file=sys.stderr)

    if failures:
        print(f"Done with failures: {len(failures)}/{len(ulg_files)}", file=sys.stderr)
        return 1

    print(f"Done: converted {len(ulg_files)} logs into: {output_base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
