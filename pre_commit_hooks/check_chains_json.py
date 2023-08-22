from __future__ import annotations

import argparse
import json
from typing import Any
from typing import Sequence

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

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        with open(filename, 'rb') as f:
            try:
                chains_json = json.load(f)
                check_asset_ids(chains_json)
                check_node_is_unique(chains_json)
            except ValueError as exc:
                print(f'{filename}: Found problems - ({exc})')
                retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
