from pathlib import Path

def has_obsidian_frontmatter(filepath: Path) -> bool:
    """
    Check if a markdown file contains Obsidian (YAML) frontmatter.

    Adheres to Obsidian's requirement that frontmatter must start
    on the very first line of the file.
    """
    try:
        with filepath.open("r", encoding="utf-8") as file:
            first_line = file.readline().strip()

            # The frontmatter MUST start on the very first line
            if first_line != "---":
                return False

            # Efficiently iterate through lines to find the closing '---'
            for line in file:
                if line.strip() == "---":
                    return True

            return False

    except (UnicodeDecodeError, OSError):
        # Catches encoding issues or system-level file access errors
        return False

def add_password_to_frontmatter(filepath: Path, password: str = "HIDE_FROM_PLAYERS") -> None:
    """Add a password to the Obsidian frontmatter of a markdown file."""
    try:
        # If we get to here we know the file has frontmatter, so we can safely add the password
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        # Find the end of the frontmatter
        for i in range(1, len(lines)):
            if not lines[i].strip() == "---":
                continue
            # Check if the password line already exists to avoid duplicates
            if any(line.startswith("password:") for line in lines[1:i]):
                # count how many password lines there are
                password_count = sum(1 for line in lines[1:i] if line.startswith("password:"))
                # remove all password lines to prevent duplicates, we will add the new one later
                lines = [line for line in lines if not line.startswith("password:")]
                # this changes the index of the closing '---', so we need to adjust it accordingly
                i -= password_count
            # Insert the password line before the closing '---'
            lines.insert(i, f"password: {password}")
            break
        # Write the modified content back to the file
        filepath.write_text("\n".join(lines), encoding="utf-8")

    except (UnicodeDecodeError, OSError) as e:
        print(f"Error processing file {filepath}: {e}")

def add_frontmatter(filepath: Path) -> None:
    """Add Obsidian frontmatter to a markdown file that lacks it."""
    try:
        content = filepath.read_text(encoding="utf-8")
        # Prepend the frontmatter to the existing content
        new_content = f"---\ntitle: {filepath.stem}\n---\n{content}"
        filepath.write_text(new_content, encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        print(f"Error processing file {filepath}: {e}")

def main(vault_path: Path|str = "./content") -> None:
    """Entry point for vault scanning."""
    if isinstance(vault_path, str):
        vault_path = Path(vault_path)

    if not vault_path.exists():
        print(f"Error: Path {vault_path} does not exist.")
        return

    # rglob is more efficient and readable than glob.glob for recursive searches
    markdown_files = [file for file in vault_path.rglob("*.md") if "Player Notes" not in file.parts]

    results = {"with": 0, "without": 0}

    for md_file in markdown_files:
        if has_obsidian_frontmatter(md_file):
            results["with"] += 1
            add_password_to_frontmatter(md_file)
        else:
            add_frontmatter(md_file)
            add_password_to_frontmatter(md_file)
            results["without"] += 1

    print(f"Total Markdown files: {len(markdown_files)}")
    print(f"Files WITH frontmatter: {results['with']}")
    print(f"Files WITHOUT frontmatter: {results['without']}")

if __name__ == "__main__":
    main()