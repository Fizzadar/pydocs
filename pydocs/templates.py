# pydocs
# File: templates.py
# Desc: jinja templates outputting markdown

from jinja2 import Template


function_template = Template('''
##### {{ module }}.{% if class %}{{ class }}.{% endif %}{{ name }}
{% if doc_string %}

{{ doc_string }}
{% endif %}

```py
{% if class %}{{ class }}.{% endif %}{{ name }}({% if args %}

{% for arg in args %}
    {{ arg }}{% if arg in defaults %}={{ defaults[arg] }}{% endif %}{% if not loop.last %},{% endif %}

{% endfor %}
{% if varargs %}
    *{{ varargs }}
{% endif %}
{% if kwargs %}
    **{{ kwargs }}
{% endif %}
{% endif %})
```

''', trim_blocks=True)

def test(thing):
    print thing
