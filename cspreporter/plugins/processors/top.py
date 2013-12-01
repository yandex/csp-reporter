import sqlite3

from cspreporter.core.plugins import Processor

class Top(Processor):
    title = 'Top Blocked URIs'
    desc = 'Determines most blocked URIs'
    limit = 10

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
        c.execute('CREATE UNIQUE INDEX blocked_uri_idx ON csp_reports (blocked_uri)')

    def process(self, report):
        if not report.blocked_uri:
            return
        c = self.conn.cursor()
        r = c.execute('UPDATE csp_reports SET count=count+1 WHERE blocked_uri = ?', (report.blocked_uri,))
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
            result += '\n``' + row['blocked_uri'] + '`` (' + str(row['count']) + ')'
            result += '\n\n* document-uri: ``' + row['document_uri'].strip() + '``'
            result += '\n* violated-directive: ``' + row['violated_directive'].strip() + '``'
            if row['referrer']:
                result += '\n* referrer: ``' + row['referrer'].strip() + '``'
            result += '\n\n'
        return result

    def teardown(self):
        pass
