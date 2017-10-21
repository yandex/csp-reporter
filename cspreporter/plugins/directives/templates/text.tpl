{% for directive, rows in directives.items() %}
### {{ directive }}
{% for row in rows %}

`{{ row.blocked_uri }}` ( row.count )
* document-uri: `{{ row.document_uri }}`
* violated-directive: `{{ row.violated_directive }}`
{% if  row.referrer %}
* referrer: `{{ row.referrer }}`
{% endif %}
{% endfor %}
{% endfor %}

<!-- 
vim: ft=markdown
-->
