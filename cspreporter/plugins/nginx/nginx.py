from cspreporter.core.plugins import LogFormat
import json

class Nginx(LogFormat):
    title = 'Clean up log'
    desc = 'This plugin cleans up log entries to JSON data only'

    def setup(self):
        pass

    def process(self, s):
        tmp = s.decode('unicode-escape')
        return tmp[tmp.rfind('{"csp-report"'):].strip('"\n ')

    def teardown(self):
        pass
