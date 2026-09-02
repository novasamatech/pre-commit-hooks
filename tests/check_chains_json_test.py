from __future__ import annotations

import json

import pytest

from pre_commit_hooks.check_chains_json import main


def _chain(nodes):
    return {
        'chainId': '0xdeadbeef',
        'name': 'Test Chain',
        'assets': [{'assetId': 0, 'symbol': 'TST', 'precision': 12}],
        'nodes': nodes,
    }


def _write(tmpdir, chains):
    f = tmpdir.join('chains.json')
    f.write(json.dumps(chains))
    return str(f)


@pytest.mark.parametrize(
    ('nodes', 'expected_retval'), (
        ([{'url': 'wss://rpc.example.org', 'name': 'wss node'}], 0),
        ([{'url': 'ws://rpc.example.org', 'name': 'ws node'}], 0),
        (
            [
                {'url': 'https://rpc.example.org', 'name': 'http node'},
                {'url': 'wss://rpc.example.org', 'name': 'wss node'},
            ],
            0,
        ),
        ([{'url': 'https://rpc.example.org', 'name': 'http node'}], 1),
        ([], 1),
    ),
)
def test_chain_requires_wss_node(capsys, tmpdir, nodes, expected_retval):
    ret = main([_write(tmpdir, [_chain(nodes)])])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert 'Test Chain' in stdout
        assert 'no ws:// or wss:// node' in stdout


def test_entries_without_nodes_are_ignored(tmpdir):
    f = tmpdir.join('not_chains.json')
    f.write(json.dumps([{'name': 'some dapp', 'url': 'https://example.org'}]))
    assert main([str(f)]) == 0
