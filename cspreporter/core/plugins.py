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
        self._generate_report(processors)
        
    def _generate_report(self, processors):
        pass

    def teardown(self):
        raise NotImplementedError

class LogFormat(BasePlugin):
    ptype = 'logformat'

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
