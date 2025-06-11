from __future__ import annotations

import argparse
import json
import os
import re
from typing import Sequence
from pathlib import Path


def check_asset_ids(chains: list) -> None:
    for chain in chains:
        seen_ids = set()
        if 'assets' in chain:
            for asset in chain['assets']:
                if asset['assetId'] in seen_ids:
                    raise ValueError(f"Duplicate id '{asset['assetId']}' found.")
                else:
                    seen_ids.add(asset['assetId'])

def check_node_is_unique(chains: list) -> None:
    for chain in chains:
        seen_urls = set()
        if 'nodes' in chain:
            for node in chain['nodes']:
                if node['url'] in seen_urls:
                    raise ValueError(f"Duplicate url '{node['url']}' found.")
                else:
                    seen_urls.add(node['url'])

def check_icon_existence(chains: list) -> None:
    for chain in chains:
        if 'assets' in chain:
            for asset in chain['assets']:
                if 'icon' in asset:
                    icon_path = Path('icons') / 'tokens' / 'colored' / asset['icon']
                    if not icon_path.is_file():
                        raise ValueError(f"Icon file '{asset['icon']}' not found in 'icons/tokens/colored' directory.")

def check_currency_id_scale(chains: list) -> None:
    for chain in chains:
        seen_scales = set()
        if 'assets' in chain:
            for asset in chain['assets']:
                if 'typeExtras' in asset and 'currencyIdScale' in asset['typeExtras']:
                    scale = asset['typeExtras']['currencyIdScale']
                    if scale in seen_scales:
                        raise ValueError(f"Duplicate currencyIdScale '{scale}' found.")
                    else:
                        seen_scales.add(scale)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            try:
                chains_json = json.load(f)
                if isinstance(chains_json, list):
                    check_asset_ids(chains_json)
                    check_currency_id_scale(chains_json)
                    check_node_is_unique(chains_json)
                    
                    # Check if filename includes a version
                    version_match = re.search(r'v(\d+)', filename)
                    if version_match:
                        version = int(version_match.group(1))
                        if version >= 21:
                            check_icon_existence(chains_json)

            except ValueError as exc:
                print(f'{filename}: Found problems - ({exc})')
                retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
