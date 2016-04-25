from cspreporter.core.plugins import LogFormat

class Simple(LogFormat):
    title = 'Clean up log'
    desc = 'This plugin cleans up log entries to JSON data only'

    def setup(self):
        pass

    def process(self, s):
        tmp = s.decode()
        return tmp[tmp.rfind('{"csp-report"'):]

    def teardown(self):
        pass
