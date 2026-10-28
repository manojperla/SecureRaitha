"""Dependency-free lab launcher. Metadata uses the JSON subset of YAML."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from tooling.verify import verify

ROOT = Path(__file__).resolve().parent


def catalog():
    entries = []
    for path in sorted((ROOT / 'labs').rglob('lab.yaml')):
        item = json.loads(path.read_text(encoding='utf-8'))
        item['path'] = path.parent.relative_to(ROOT).as_posix()
        entries.append(item)
    if len({item['id'] for item in entries}) != len(entries):
        raise ValueError('Duplicate lab IDs')
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['list', 'catalog', 'up', 'down', 'reset', 'verify'])
    parser.add_argument('id', nargs='?')
    parser.add_argument('--fixed', action='store_true', help='launch or verify the remediated variant')
    parser.add_argument('--purge', action='store_true', help='remove Compose volumes when stopping')
    args = parser.parse_args()
    entries = catalog()
    if args.command == 'catalog':
        (ROOT / 'catalog.yaml').write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
        return
    if args.command == 'list':
        for item in entries:
            print(f"{item['id']:55} {item['title']}")
        return
    item = next((entry for entry in entries if entry['id'] == args.id), None)
    if item is None:
        parser.error('Supply a lab ID from: python lab.py list')
    if args.command == 'verify':
        verify(item['category'], item['port'], args.fixed)
        print('PASS: ' + item['id'] + (' (fixed)' if args.fixed else ' (vulnerable)'))
        return
    if shutil.which('docker') is None:
        raise RuntimeError('Docker with Compose is required for deployment. See README.md.')
    command = ['docker', 'compose', '-p', 'sr-' + item['id'].replace('.', '-'),
               '-f', str(ROOT / item['path'] / 'compose.yaml')]
    env = dict(os.environ, LAB_FIXED='1' if args.fixed else '0')
    if args.command in ('down', 'reset'):
        subprocess.run(command + ['down'] + (['--volumes'] if args.purge or args.command == 'reset' else []), env=env, check=True)
    if args.command in ('up', 'reset'):
        subprocess.run(command + ['up', '-d', '--build', '--force-recreate'], env=env, check=True)
        deadline = time.monotonic() + 30
        while True:
            try:
                verify(item['category'], item['port'], args.fixed)
                break
            except (OSError, RuntimeError):
                if time.monotonic() >= deadline:
                    raise RuntimeError('Lab verification timed out; inspect docker compose logs or run down --purge.')
                time.sleep(0.5)
        print(f"Ready and verified: {item['id']} on 127.0.0.1:{item['port']}")


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)
