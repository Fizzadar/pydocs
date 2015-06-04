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
    {{ arg }}{% if arg in defaults %}={{ defaults[arg] }}{% endif %}
{% if not loop.last or varargs or kwargs %},{% endif %}{% if arg in arg_comments %} # {{ arg_comments[arg] }}{% endif %}

{% endfor %}
{% if varargs %}
    {{ varargs }}{% if kwargs %},{% if varargs in arg_comments %} # {{ arg_comments[varargs] }}{% endif %}

{% else %}

{% endif %}
{% endif %}
{% if kwargs %}
    {{ kwargs }}{% if kwargs in arg_comments %} # {{ arg_comments[kwargs] }}{% endif %}

{% endif %}
{% endif %})
```

''', trim_blocks=True)
