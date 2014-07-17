#!/usr/bin/env python3

import configparser
import argparse
import json
import time

from cspreporter.core.util import OuputManager
from cspreporter.core.util import load_plugin
from cspreporter.core.util import CSPReport

start = time.time()

plugins = {}
plugins['preprocessors'] = []
plugins['processors'] = []
plugins['output'] = []
config_file = 'config.ini'

parser = argparse.ArgumentParser(
            description = 'CSP Reporter',
            epilog = 'Tested on MacOS and Linux')
parser.add_argument('-c', '--config',
            metavar = 'FILENAME',
            dest='config',
            help = 'Configuration file')
parser.add_argument('-f', '--filename',
            metavar = 'FILENAME',
            dest='filename',
            required = True,
            help = 'Input filename')
args = parser.parse_args()

if args.config:
    config_file = args.config

config = configparser.ConfigParser()
config.read(config_file)
om = OuputManager(config.getboolean('common', 'debug'))

om.dbg('Loading plugins...')
for sec in config.sections():
    if not sec.startswith('plugins.'):
        continue
    chunks = sec.split('.')
    plugins[chunks[1]].append(load_plugin(chunks[2], chunks[1], config))

om.dbg('Seting up plugins...')
for t in plugins:
    for p in plugins[t]:
        p.setup()

om.dbg('Processing report ' + args.filename)
logfile = open(args.filename, 'r')
line = logfile.readline()

while line:
    if plugins['preprocessors']:
        line = plugins['preprocessors'][0].process(line)
    r = CSPReport()
    try:
        r.load_from_string(line)
    except Exception as e:
        line = logfile.readline()
        continue
    for p in plugins['processors']:
        p.process(r)
    line = logfile.readline()

om.dbg('Generating report')
for r in plugins['output']:
    r.generate_report(plugins['processors'])

om.dbg('Teardown plugins...')
for t in plugins:
    for p in plugins[t]:
        p.teardown()

om.dbg('The end!')
om.dbg("Time: %.01f s" % (time.time() - start))
