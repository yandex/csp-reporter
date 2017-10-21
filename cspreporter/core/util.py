import importlib
import json

import configparser
CONFIG = None


def load_plugin(pname, config):
    m = importlib.import_module('cspreporter.plugins.' + pname + '.' + pname)
    pclassname = ''.join([i.title() for i in pname.split('_')])
    return getattr(m, pclassname)(config)


def load_plugins(config):
    plugins = {}
    plugins['logformat'] = []
    plugins['processor'] = []
    plugins['output'] = []

    for sec in config.sections():
        if not sec.startswith('plugins.'):
            continue
        pname = sec.split('.')[1]
        i = load_plugin(pname, config)
        i.setup()
        plugins[i.ptype].append(i)

    if not plugins['logformat']:
        plugins['logformat'].append(load_plugin('simple', config))

    return plugins


def get_config(config_file='config.ini'):
    global CONFIG
    if not CONFIG:
        CONFIG = configparser.ConfigParser()
        CONFIG.read(config_file)
    return CONFIG
