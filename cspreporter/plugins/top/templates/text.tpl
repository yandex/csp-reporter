{% for row in rows %}

`{{ row.blocked_uri }}` ( row.count )
* document-uri: `{{ row.document_uri }}`
* violated-directive: `{{ row.violated_directive }}`
{% if  row.referrer %}
* referrer: `{{ row.referrer }}`
{% endif %}
{% endfor %}

<!-- 
vim: ft=markdown
-->
