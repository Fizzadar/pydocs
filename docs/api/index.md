## pydocs


##### pydocs.build

Build markdown documentation from a directory and/or python module.

# ignore_modules: takes a list of module names to ignore
# index_filename: __init__.py output (default index.md), use README.md for github indexes

```py
build(
    root,
    source_module,
    output_dir,
    json_dump=False,
    ignore_modules=None,
    index_filename='index'
)
```


##### pydocs.main

Main in a function in case you place a build.py for pydocs inside the root directory.

```py
main()
```
