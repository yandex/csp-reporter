import json


class CSPReport(object):
    def __init__(self):
        self.directives = {}
        self.directives['blocked-uri'] = ''
        self.directives['document-uri'] = ''
        self.directives['original-policy'] = ''
        self.directives['referrer'] = ''
        self.directives['source-file'] = ''
        self.directives['status-code'] = ''
        self.directives['violated-directive'] = ''

    def __getattr__(self, name):
        n = name.replace('_', '-')
        if n in self.directives:
            return self.directives[n]
        raise AttributeError

    def load_from_string(self, s, logformat):
        result = False
        data = logformat.process(s).strip()
        try:
            j = json.loads(data)
        except:
            return result
        for d in self.directives:
            if d in j['csp-report']:
                self.directives[d] = j['csp-report'][d]
                result = True
        return result
