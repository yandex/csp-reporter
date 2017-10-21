{% for row in rows %}

`{{ row.document_uri }}` ( row.count )
* blocked-uri: `{{ row.blocked_uri }}`
{% if  row.referrer %}
* referrer: `{{ row.referrer }}`
{% endif %}
{% endfor %}

<!-- 
vim: ft=markdown
-->
