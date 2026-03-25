"""
A script to recursively merge all Markdown files from an Obsidian vault.
Compliant with Ruff linting and modern Python best practices.
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def combine_obsidian_vault(
    vault_dir: str | Path,
    output_file: str | Path
) -> None:
    """
    Recursively finds all .md files in a directory and merges them.

    Args:
        vault_dir: Path to the root of the Obsidian vault.
        output_file: Path/name of the resulting merged file.
    """
    vault_path = Path(vault_dir).resolve()
    output_path = Path(output_file).resolve()

    if not vault_path.is_dir():
        logging.error(f"Vault directory not found: {vault_path}")
        return

    # Using a list to track processed files for a final summary
    processed_count = 0

    try:
        with output_path.open("w", encoding="utf-8") as outfile:
            # .rglob("*.md") recursively finds all markdown files
            for md_file in vault_path.rglob("*.md"):
                # Prevent the script from reading its own output if stored in the vault
                if md_file == output_path:
                    continue

                processed_count += 1
                relative_path = md_file.relative_to(vault_path)

                # Write metadata headers for context
                outfile.write(f"\n\n{'='*40}\n")
                outfile.write(f"FILE: {relative_path}\n")
                outfile.write(f"{'='*40}\n\n")

                # Read and append content
                content = md_file.read_text(encoding="utf-8")
                outfile.write(content)

                # Ensure there is a newline between files
                if not content.endswith("\n"):
                    outfile.write("\n")

        logging.info(f"Successfully merged {processed_count} files into {output_path}")

    except PermissionError:
        logging.error("Permission denied. Ensure the output file is not open.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Replace with your actual path. Use forward slashes even on Windows.
    VAULT_LOCATION = "./content/"
    RESULT_NAME = "Merged_Obsidian_Notes.md"

    combine_obsidian_vault(VAULT_LOCATION, RESULT_NAME)