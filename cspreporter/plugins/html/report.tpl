<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>CSP Report</title>
    <style type="text/css">
    body {
        background: #dcddd8;
        color: #354b5e;
        font-family: arial, sans-serif;
        margin: 0;
        padding: 2em;
    }

    a {color: #475f77;}

    h1.title {
        text-align: center;
        color: #d74b4b;
        font-size: 2.5em;
        background-color: #dcddd8;
    }

    h1 a, h2 a, h3 a { 
        color: white;
        text-decoration: none;
    }

    h1 {
        background-color: #d74b4b;
        color: white;
        font-size: 1.3em;
        padding: 0.2em;
    }

    h2 {
        background-color: #d74b4b;
        color: white;
        font-size: 1.1em;
        padding: 0.5em;
        border-radius: 0.3em;
    }

    h3 {color: #d74b4b; font-size: 1.0em;}
    .pre {font-family: courier, monospace; font-size: 0.9em;}
    </style>
</head>
<body>
    <h1 class="title">CSP Report</h1>
    {% for plugin in plugins %}
        <h2>{{ plugin.title }}</h2>
        {{ plugin.html | safe }}
    {% endfor %}
    <hr />
    <p>Generated with <a href="https://www.oxdef.info/csp-reporter">CSP Reporter</a></p>
</body>
</html>

<!-- 
vim: ft=html
-->
