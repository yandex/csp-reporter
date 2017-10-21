import sqlite3
import os

from jinja2 import Environment, FileSystemLoader

from cspreporter.core.plugins import Processor
from cspreporter.plugins import ROOT_PATH


class Top(Processor):
    title = 'Top Blocked URIs'
    desc = 'Determines most blocked URIs'
    limit = 10

    def setup(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

        c = self.conn.cursor()
        c.execute('CREATE TABLE csp_reports (' +
                  'blocked_uri text,' +
                  'document_uri text,' +
                  'violated_directive text,' +
                  'original_policy text,' +
                  'referrer text,' +
                  'count integer DEFAULT 0)')
        c.execute('CREATE UNIQUE INDEX blocked_uri_idx ' +
                  'ON csp_reports (blocked_uri)')
        self.env = Environment(
            loader=FileSystemLoader(
                os.path.join(ROOT_PATH, 'top', 'templates')))

    def process(self, report):
        if not report.blocked_uri:
            return
        c = self.conn.cursor()
        r = c.execute('UPDATE csp_reports SET count=count+1 ' +
                      'WHERE blocked_uri = ?', (report.blocked_uri,))
        if not r.rowcount:
            data = (
                    report.blocked_uri,
                    report.document_uri,
                    report.violated_directive,
                    report.original_policy,
                    report.referrer
                    )
            r = c.execute('INSERT INTO csp_reports ' +
                          'VALUES (?,?,?,?,?, 1)', data)
        self.conn.commit()
        c.close()

    def get_result(self):
        result = []
        c = self.conn.cursor()
        rows = c.execute('SELECT * FROM csp_reports ' +
                         'ORDER BY count DESC LIMIT ' +
                         str(self.limit))
        for r in rows:
            result.append(r)
        return result

    def get_html(self):
        t = self.env.get_template('html.tpl')
        body = t.render(rows=self.get_result())
        return body

    def get_text(self):
        t = self.env.get_template('text.tpl')
        body = t.render(rows=self.get_result())
        return body

    def teardown(self):
        pass
