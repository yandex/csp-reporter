{% for row in rows %}
<code>{{ row.document_uri }}</code> ({{ row.count }})
<ul>
    <li>blocked-uri: <code>{{ row.blocked_uri }}</code></li>
    {% if  row.referrer %}
        <li>referrer: <code>{{ row.referrer }}</code></li>
    {% endif %}
</ul>
{% endfor %}

<!-- 
vim: ft=html
-->
