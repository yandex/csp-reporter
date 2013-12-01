import sqlite3

from cspreporter.core.plugins import Processor

class Xss(Processor):
    title = 'XSS Finder'
    desc = 'Tries to determine XSS attack'
    limit = 10
    keywords = ['<javascript']

    def setup(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        
        c = self.conn.cursor()
        c.execute('''CREATE TABLE csp_reports (
                blocked_uri text, 
                document_uri text, 
                violated_directive text, 
                original_policy text, 
                referrer text, 
                count integer DEFAULT 0
                )''')
        c.execute('CREATE UNIQUE INDEX document_uri_idx ON csp_reports (document_uri)')

    def process(self, report):
        if not report.violated_directive.startswith('script-src'):
            return

        for k in self.keywords:
            if k in report.document_uri:
                break
        else:
            return

        c = self.conn.cursor()
        r = c.execute('UPDATE csp_reports SET count=count+1 WHERE document_uri = ?', (report.document_uri,))
        if not r.rowcount:
            data = (
                    report.blocked_uri,
                    report.document_uri,
                    report.violated_directive,
                    report.original_policy,
                    report.referrer
                    )
            r = c.execute('INSERT INTO csp_reports VALUES (?,?,?,?,?, 1)', data)
        self.conn.commit()
        c.close()

    def get_result(self):
        result = ''
        c = self.conn.cursor()
        rows = c.execute('SELECT * FROM csp_reports ORDER BY count DESC LIMIT ' + str(self.limit))
        for row in rows:
            result += '\n' + row['document_uri'] + ' (' + str(row['count']) + ')'
            result += '\n' + '-'*(len(str(row['count']) + row['blocked_uri']) + 5) 
            result += '\nblocked-uri: ``' + row['blocked_uri'] + '``'
            if row['referrer']:
                result += '\nreferrer: ``' + row['referrer'] + '``'
            result += '\n'
        return result

    def teardown(self):
        pass
