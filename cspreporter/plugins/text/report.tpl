## CSP Report

{% for plugin in plugins %}
## {{ plugin.title }}
    {{ plugin.text | safe }}
{% endfor %}

----
Generated with [CSP Reporter](https://www.oxdef.info/csp-reporter)
<!-- 
vim: ft=markdown
-->
