import os

from jinja2 import Environment, FileSystemLoader

from cspreporter.core.plugins import Output
from cspreporter.plugins import ROOT_PATH

class Console(Output):
    title = 'Console output'
    desc = 'Console plugin outputs report data to the stdout'

    def setup(self):
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
        print(body)

    def teardown(self):
        pass
