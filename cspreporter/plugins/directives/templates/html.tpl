{% for directive, rows in directives.items() %}
    <h3>{{ directive }}</h3>
    {% for row in rows %}
    <code>{{ row.blocked_uri }}</code> ({{ row.count }})
    <ul>
        <li>document-uri: <code>{{ row.document_uri }}</code></li>
        <li>violated-directive: <code>{{ row.violated_directive }}</code></li>
        {% if  row.referrer %}
            <li>referrer: <code>{{ row.referrer }}</code></li>
        {% endif %}
    </ul>
    {% endfor %}
{% endfor %}

<!-- 
vim: ft=html
-->
