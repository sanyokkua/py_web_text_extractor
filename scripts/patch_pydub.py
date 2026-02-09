#!/usr/bin/env python3

"""
Patch pydub library for Python 3.13+ compatibility.

Fixes invalid escape sequences in regex patterns.
"""

import sys
from pathlib import Path


def find_pydub_utils() -> Path:
    """Locate pydub/utils.py in the current environment."""
    try:
        import pydub

        return Path(pydub.__file__).parent / "utils.py"
    except ImportError:
        print("❌ pydub is not installed", file=sys.stderr)
        sys.exit(1)


def patch_file(file_path: Path) -> bool:
    """Patch the file by fixing invalid escape sequences."""
    if not file_path.exists():
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        return False

    original_content = file_path.read_text()
    patched_content = original_content

    # Fix 1: Line ~300 - invalid escape sequence '\('
    patched_content = patched_content.replace(
        r"m = re.match('([su]([0-9]{1,2})p?) \(([0-9]{1,2}) bit\)$', token)",
        r"m = re.match(r'([su]([0-9]{1,2})p?) \(([0-9]{1,2}) bit\)$', token)",
    )

    # Fix 2: Any other occurrences of '\(' or '\)' in string literals
    # Using a more general approach for safety
    patched_content = patched_content.replace(r"'\(", r"'\\(")
    patched_content = patched_content.replace(r"\)'", r"\\)'")

    # Check if changes were made
    if patched_content == original_content:
        print("✓ pydub/utils.py is already patched or doesn't need patching")
        return False

    # Create backup
    backup_path = file_path.with_suffix(".py.bak")
    backup_path.write_text(original_content)
    print(f"✓ Created backup: {backup_path}")

    # Write patched content
    file_path.write_text(patched_content)
    print("✓ Successfully patched pydub/utils.py for Python 3.13+ compatibility")
    return True


def main():
    print("🔧 Patching pydub for Python 3.13+ compatibility...")
    utils_path = find_pydub_utils()
    print(f"📁 Target file: {utils_path}")

    patched = patch_file(utils_path)

    if patched:
        print("✅ Patch applied successfully")
        return 0
    else:
        print("ℹ️  No changes needed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
