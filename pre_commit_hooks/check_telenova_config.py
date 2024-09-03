from __future__ import annotations

import argparse
import json
from typing import Sequence

def check_chain_id_is_unique(chains: list) -> None:
  seen_ids = set()
  for chain in chains:
    if 'chainIndex' in chain:
      if chain['chainIndex'] in seen_ids:
        raise ValueError(f"Duplicate id '{chain['chainIndex']}' found.")
      else:
        seen_ids.add(chain['chainIndex'])
    else:
      raise ValueError(f"Missing 'chainIndex' in chain '{chain}'")


def main(argv: Sequence[str] | None = None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument('filenames', nargs='*', help='Filenames to check.')
  args = parser.parse_args(argv)

  retval = 0
  for filename in args.filenames:
    with open(filename, 'rb') as f:
      try:
        telenova_config = json.load(f)
        if isinstance(telenova_config, list):
          check_chain_id_is_unique(telenova_config)
      except ValueError as exc:
        print(f'{filename}: Found problems - ({exc})')
        retval = 1
  return retval


if __name__ == '__main__':
  raise SystemExit(main())
