import os

from jinja2 import Environment, FileSystemLoader

from cspreporter.core.plugins import Output
from cspreporter.plugins import ROOT_PATH

class Html(Output):
    title = 'HTML file output'
    desc = 'HTML plugin outputs report data to the file specified in config'

    def setup(self):
        self.filename = self.config.get('plugins.html', 'filename')
        self._fh = open(self.filename, 'w')
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(ROOT_PATH, 'html')))

    def _generate_report(self, processors):
        plugins = []
        for p in processors:
            plugin = {}
            plugin['title'] = p.title
            plugin['html'] = p.get_html()
            plugins.append(plugin)            
        t = self.env.get_template('report.tpl')
        body = t.render(plugins=plugins)
        self._fh.write(body)

    def teardown(self):
        self._fh.close()





