import sqlite3
from urllib.parse import urlparse

from cspreporter.core.plugins import Processor

class Directives(Processor):
    title = 'Top Blocked URIs by Directives'
    desc = 'Determines most blocked URIs with hostnames filtered by directives'
    limit = 10
    directives = []

    def setup(self):
        k = self.config.get('plugins.processors.directives', 'directives')
        chunks = k.split(',')
        self.directives = [i.strip() for i in chunks]
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
        c.execute('CREATE UNIQUE INDEX blocked_uri_idx ON csp_reports (blocked_uri)')

    def process(self, report):
        directive = None
        if not report.violated_directive:
            return
 
        if not report.blocked_uri:
            return
        
        for d in self.directives:
            if report.violated_directive.startswith(d):
                directive = d
                break
        else:
            return

        c = self.conn.cursor()
        r = c.execute('UPDATE csp_reports SET count=count+1 WHERE blocked_uri = ?', (report.blocked_uri,))
        if not r.rowcount:
            data = (
                    report.blocked_uri,
                    report.document_uri,
                    directive,
                    report.original_policy,
                    report.referrer
                    )
            r = c.execute('INSERT INTO csp_reports VALUES (?,?,?,?,?, 1)', data)
        self.conn.commit()
        c.close()

    def get_result(self):
        result = ''
        c = self.conn.cursor()

        for d in self.directives:
            result +='\n' + d + '\n'
            result += '~' * len(d) + '\n\n'
            rows = c.execute('SELECT * FROM csp_reports WHERE violated_directive=? ORDER BY count DESC LIMIT ' + str(self.limit), (d, ))
            for row in rows:
                result += '\n``' + row['blocked_uri'] + '`` (' + str(row['count']) + ')'
                result += '\n\n* document-uri: ``' + row['document_uri'].strip() + '``'
                if row['referrer']:
                    result += '\n* referrer: ``' + row['referrer'].strip() + '``'
                result += '\n\n'
        return result

    def teardown(self):
        pass
