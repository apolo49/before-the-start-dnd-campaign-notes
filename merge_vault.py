
"""
Recursively merge Markdown files from an Obsidian vault,
optionally splitting the output into multiple files.

Usage:
    python merge_obsidian.py
    python merge_obsidian.py --pages 100
    python merge_obsidian.py --vault ./content --output Merged_Notes.md --pages 50
"""

import argparse
import logging
import re
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def combine_obsidian_vault(
    vault_dir: str | Path,
    output_file: str | Path,
    pages_per_file: int | None = None,
) -> None:
    """
    Merge Markdown files from a vault into one or more output files.

    Args:
        vault_dir: Root directory of the Obsidian vault.
        output_file: Output filename, used as the base name for split files.
        pages_per_file: Maximum original Markdown files per output file.
            None means merge all files into a single output file.
    """
    vault_path = Path(vault_dir).resolve()
    output_path = Path(output_file).resolve()

    if not vault_path.is_dir():
        logging.error("Vault directory not found: %s", vault_path)
        return

    if pages_per_file is not None and pages_per_file < 1:
        logging.error("Pages per file must be at least 1.")
        return

    try:
        # Find all Markdown files in deterministic order.
        md_files = sorted(
            vault_path.rglob("*.md"),
            key=lambda path: path.relative_to(vault_path).as_posix().casefold(),
        )

        # Exclude existing output files if the output is inside the vault.
        # This prevents previous merge results from being merged again.
        output_pattern = re.compile(
            rf"^{re.escape(output_path.stem)}(?:_\d+)?"
            rf"{re.escape(output_path.suffix)}$"
        )

        md_files = [
            path
            for path in md_files
            if not (
                path.resolve() == output_path
                or (
                    path.parent.resolve() == output_path.parent
                    and output_pattern.fullmatch(path.name)
                )
            )
        ]

        if not md_files:
            logging.warning("No Markdown files found in %s", vault_path)
            return

        # Split the source files into batches, if requested.
        batch_size = pages_per_file or len(md_files)
        batches = [
            md_files[index : index + batch_size]
            for index in range(0, len(md_files), batch_size)
        ]

        output_path.parent.mkdir(parents=True, exist_ok=True)

        for batch_index, batch in enumerate(batches, start=1):
            if pages_per_file is None:
                current_output = output_path
            else:
                current_output = output_path.with_name(
                    f"{output_path.stem}_{batch_index:03d}"
                    f"{output_path.suffix or '.md'}"
                )

            with current_output.open("w", encoding="utf-8") as outfile:
                for md_file in batch:
                    relative_path = md_file.relative_to(vault_path)
                    content = md_file.read_text(encoding="utf-8")

                    # Write a header identifying the original file.
                    outfile.write(f"\n\n{'=' * 40}\n")
                    outfile.write(f"FILE: {relative_path}\n")
                    outfile.write(f"{'=' * 40}\n\n")
                    outfile.write(content)

                    if not content.endswith("\n"):
                        outfile.write("\n")

            logging.info(
                "Created %s (%d of %d source files)",
                current_output,
                len(batch),
                len(md_files),
            )

        logging.info(
            "Successfully merged %d Markdown files into %d output file(s).",
            len(md_files),
            len(batches),
        )

    except PermissionError:
        logging.exception(
            "Permission denied. Check file permissions and whether an output "
            "file is open in another application."
        )
    except OSError:
        logging.exception("An error occurred while reading or writing files.")


def main() -> None:
    """Parse command-line arguments and run the merge."""
    parser = argparse.ArgumentParser(
        description="Merge an Obsidian vault into one or more Markdown files."
    )
    parser.add_argument(
        "--vault",
        default="./content/",
        help="Path to the Obsidian vault (default: ./content/).",
    )
    parser.add_argument(
        "--output",
        default="Merged_Obsidian_Notes.md",
        help="Output filename (default: Merged_Obsidian_Notes.md).",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Maximum number of original Markdown files per merged file. "
            "Defaults to all files in one output."
        ),
    )

    args = parser.parse_args()

    if args.pages is not None and args.pages < 1:
        parser.error("--pages must be a positive integer.")

    combine_obsidian_vault(
        vault_dir=args.vault,
        output_file=args.output,
        pages_per_file=args.pages,
    )


if __name__ == "__main__":
    main()
