import importlib
import json

class CSPReport(object):
    def __init__(self):
        self.directives = {}
        self.directives['blocked-uri'] = ''
        self.directives['document-uri'] = '' 
        self.directives['original-policy'] = '' 
        self.directives['referrer']= ''
        self.directives['source-file'] = '' 
        self.directives['status-code'] = '' 
        self.directives['violated-directive'] = ''

    def __getattr__(self, name):
        n = name.replace('_', '-')
        if n in self.directives:
            return self.directives[n]
        raise AttributeError

    def load_from_string(self, s):
        j = json.loads(s.strip())
        for d in self.directives:
            if d in j['csp-report']:
                self.directives[d] = j['csp-report'][d]

def load_plugin(pname, ptype, config):
    m = importlib.import_module('cspreporter.plugins.' + ptype + '.' + pname)
    pclassname = ''.join([i.title() for i in pname.split('_')])
    return getattr(m, pclassname)(config)

class OuputManager:
    debug = False

    def __init__(self, debug=False):
        self.debug = debug

    def dbg(self, s):
        if self.debug: 
            print(s)
