class BasePlugin(object):
    config = None
    ptype = None
    title = 'Base plugin'
    desc = 'Some text about base plugin'
    
    def __init__(self, config):
        self.config = config

    def setup(self):
        """called before the plugin is asked to do anything"""
        raise NotImplementedError

    def teardown(self):
        """called to allow the plugin to free anything"""
        raise NotImplementedError

class Output(BasePlugin):
    ptype = 'output'
    rst_data = ''

    def setup(self):
        raise NotImplementedError

    def generate_report(self, processors):
        self.rst_data += '''=============\nCSP Report\n=============\n'''
        self.rst_data += '''\n.. contents::\n\n'''
        for p in processors:
            self.rst_data += '\n' +p.title + '\n'
            self.rst_data += "=" * (len(p.title) + 5) + '\n'
            tmp_result = p.get_result()
            if tmp_result:
                self.rst_data += tmp_result + '\n'
            else:
                self.rst_data +='\n*There is no results.*\n'
        self.rst_data += '\n\n\n----\n\n'
        self.rst_data += '''Generated with `CSP Reporter <https://www.oxdef.info/csp-reporter>`__'''
        self._generate_report(processors)
        
    def _generate_report(self, processors):
        pass

    def teardown(self):
        raise NotImplementedError

class Preprocessor(BasePlugin):
    ptype = 'preprocessor'

    def setup(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError

class Processor(BasePlugin):
    ptype = 'processor'

    def setup(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def teardown(self):
        raise NotImplementedError
