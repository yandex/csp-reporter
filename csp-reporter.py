#!/usr/bin/env python3
import argparse
import sys

from cspreporter.core.util import load_plugins
from cspreporter.core.util import get_config
from cspreporter.core.csp import CSPReport

sys.dont_write_bytecode = True

config_file = 'config.ini'

parser = argparse.ArgumentParser(
    description='CSP Reporter',
    epilog='Tested on MacOS and Linux')
parser.add_argument(
    '-c', '--config',
    metavar='FILENAME',
    dest='config',
    help='Configuration file')
parser.add_argument(
    '-f', '--filename',
    metavar='FILENAME',
    dest='filename',
    required=True,
    help='Input filename')
args = parser.parse_args()

if args.config:
    config_file = args.config

config = get_config(config_file)
plugins = load_plugins(config)

try:
    logfile = open(args.filename, 'rb')
except:
    print("Can't open report file")
    sys.exit(1)

line = logfile.readline()
while line:
    r = CSPReport()
    if not r.load_from_string(line, plugins['logformat'][0]):
        line = logfile.readline()
        continue
    for p in plugins['processor']:
        p.process(r)
    line = logfile.readline()

for r in plugins['output']:
    r.generate_report(plugins['processor'])

for t in plugins:
    for p in plugins[t]:
        p.teardown()
