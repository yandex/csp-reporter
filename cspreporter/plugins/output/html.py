import os

from docutils.core import publish_string
from docutils.writers.html4css1 import Writer as HisWriter

from cspreporter.core.plugins import Output

class Html(Output):
    title = 'HTML file output'
    desc = 'HTML plugin outputs report data to the file specified in config'

    def setup(self):
        self.filename = self.config.get('plugins.output.html', 'filename')
        self._fh = open(self.filename, 'wb')

    def _generate_report(self, processors):
        args = {
                    'stylesheet_path': os.path.join('cspreporter', 'plugins','output','html','style.css'),
        }
        self._fh.write(publish_string(self.rst_data, writer=HisWriter(), settings=None, settings_overrides=args))

    def teardown(self):
        self._fh.close()





