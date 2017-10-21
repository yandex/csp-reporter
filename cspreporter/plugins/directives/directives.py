import sqlite3
import os

from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader

from cspreporter.core.plugins import Processor
from cspreporter.plugins import ROOT_PATH


class Directives(Processor):
    title = 'Top Blocked URIs by Directives'
    desc = 'Determines most blocked URIs with hostnames filtered by directives'
    limit = 10
    directives = []

    def setup(self):
        k = self.config.get('plugins.directives', 'directives')
        chunks = k.split(',')
        self.directives = [i.strip() for i in chunks]
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
                os.path.join(ROOT_PATH, 'directives', 'templates')))

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
        r = c.execute('UPDATE csp_reports ' +
                      'SET count=count+1 ' +
                      'WHERE blocked_uri = ?', (report.blocked_uri,))
        if not r.rowcount:
            data = (
                    report.blocked_uri,
                    report.document_uri,
                    directive,
                    report.original_policy,
                    report.referrer
                    )
            r = c.execute('INSERT INTO csp_reports ' +
                          'VALUES (?,?,?,?,?, 1)', data)
        self.conn.commit()
        c.close()

    def get_result(self):
        result = {}
        c = self.conn.cursor()

        for d in self.directives:
            rows = c.execute('SELECT * FROM csp_reports ' +
                             'WHERE violated_directive=? ' +
                             'ORDER BY count DESC LIMIT ' +
                             str(self.limit), (d, ))
            result[d] = []
            for r in rows:
                result[d].append(r)
        return result

    def get_html(self):
        t = self.env.get_template('html.tpl')
        body = t.render(directives=self.get_result())
        return body

    def get_text(self):
        t = self.env.get_template('text.tpl')
        body = t.render(directives=self.get_result())
        return body

    def teardown(self):
        pass
