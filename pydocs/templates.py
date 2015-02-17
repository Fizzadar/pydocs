

function_template = '''
##### {% if class %}{{ class }}.{% endif %}{{ name }}
{% if doc_string %}

{{ doc_string }}
{% endif %}

```py
{{ module }}.{% if class %}{{ class }}.{% endif %}{{ name }}(
{% for arg in args %}
    {{ arg }}{% if arg in defaults %}={{ defaults[arg] }}{% endif %}{% if not loop.last %},{% endif %}

{% endfor %}
)
```

'''
