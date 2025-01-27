from __future__ import annotations

import argparse
import json
from typing import Sequence, Any
from pathlib import Path


def check_icon_existence_recursive(data: Any, parent_key: str = '') -> None:
    """Recursively check for 'icon' fields in any nested structure."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'icon' and isinstance(value, str):
                if value.startswith('https://raw.githubusercontent.com/'):
                    for branch in ('master/', 'main/'):
                        if branch in value:
                            value = value.split(branch, 1)[1]
                            break
                
                if parent_key == 'categories':
                    icon_path = Path(value)
                else:
                    icon_dir = 'dapps'
                    icon_path = Path('icons') / icon_dir / value
                
                if not icon_path.is_file():
                    raise ValueError(
                        f"Icon file '{value}' not found at path '{icon_path}'.",
                    )
            else:
                check_icon_existence_recursive(value, key)
    elif isinstance(data, list):
        for item in data:
            check_icon_existence_recursive(item, parent_key)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        if 'dapps' not in filename:
            continue
            
        with open(filename, 'rb') as f:
            try:
                data = json.load(f)
                check_icon_existence_recursive(data)
            except ValueError as exc:
                print(f'{filename}: Found problems - ({exc})')
                retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
