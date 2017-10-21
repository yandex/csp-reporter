import os

from jinja2 import Environment, FileSystemLoader

from cspreporter.core.plugins import Output
from cspreporter.plugins import ROOT_PATH


class Text(Output):
    title = 'Text file output'
    desc = 'Text plugin outputs report data to the file specified in config'

    def setup(self):
        self.filename = self.config.get('plugins.text', 'filename')
        self._fh = open(self.filename, 'w')
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(ROOT_PATH, 'text')))

    def _generate_report(self, processors):
        plugins = []
        for p in processors:
            plugin = {}
            plugin['title'] = p.title
            plugin['text'] = p.get_text()
            plugins.append(plugin)            
        t = self.env.get_template('report.tpl')
        body = t.render(plugins=plugins)
        self._fh.write(body)

    def teardown(self):
        self._fh.close()
