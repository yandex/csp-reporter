from cspreporter.core.plugins import Preprocessor

class Simple(Preprocessor):
    title = 'Clean up log'
    desc = 'This plugin cleans up log entries to JSON data only'

    def setup(self):
        pass

    def process(self, s):
        return s[s.rfind('{"csp-report"'):]

    def teardown(self):
        pass
