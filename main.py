#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from pathlib import Path
import subprocess
import sys
from typing import List, Sequence
import urllib.parse

_installDir = (Path(__file__) / '../').resolve()

def _parseArgs(args: Sequence[str]) -> Namespace:
  parser = ArgumentParser()
  parser.add_argument('--token-file', required=True, type=Path,
      help='Path to the file containing registration token')
  parser.add_argument('--url', required=True, type=urllib.parse.urlparse,
      help='Repository to add the runner to')
  parser.add_argument('--labels', required=False, default='',
      help='Custom labels that will be added to the runner')
  parser.add_argument('--name', required=False, default='',
      help='Name of the runner to configure')
  parser.add_argument('--work', required=False, default='',
      help='Relative runner work directory')
  return parser.parse_args(args)

def _configure(args: Namespace) -> None:
  cmd: List[str] = [
    str(_installDir / 'config.sh'), '--unattended', '--url', args.url.geturl(),
  ]
  with open(args.token_file) as tokenFile:
    cmd.append('--token')
    cmd.append(tokenFile.readline())
  if args.labels and args.labels != 'default':
    cmd.append('--labels')
    cmd.append(args.labels)
  if args.name and args.name != 'default':
    cmd.append('--name')
    cmd.append(args.name)
  if args.work and args.work != 'default':
    cmd.append('--work')
    cmd.append(args.work)
  subprocess.check_call(cmd)

def _run() -> None:
  subprocess.check_call([ str(_installDir / 'run.sh') ])

def _main() -> None:
    _configure(_parseArgs(sys.argv[1:]))
    _run()

if __name__ == '__main__':
  _main()
