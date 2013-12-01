from cspreporter.core.plugins import Output

class Text(Output):
    title = 'Text file output'
    desc = 'Text plugin outputs report data to the file specified in config'

    def setup(self):
        self.filename = self.config.get('plugins.output.text', 'filename')
        self._fh = open(self.filename, 'w')

    def _generate_report(self, processors):
        self._fh.write(self.rst_data)

    def teardown(self):
        self._fh.close()
