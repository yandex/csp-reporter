from cspreporter.core.plugins import Output

class Console(Output):
    title = 'Console output'
    desc = 'Console plugin outputs report data to the stdout'

    def setup(self):
        pass

    def _generate_report(self, processors):
        print(self.rst_data)

    def teardown(self):
        pass
