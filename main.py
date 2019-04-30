from fastapi import FastAPI
from importdir import ImportDir
import textwrap
import inspect


modules, funcs = ImportDir('./functions').do(judge=lambda module: module.endswith('_api'))
app = FastAPI()


func_list = dict()
for func in funcs:
    root_package, *path = func.split('.')
    if path:
        get_package = textwrap.dedent(f"""
            package = modules[root_package].{'.'.join(path)}
            func_list[func] = package
        """)
        exec(get_package)
    else:
        func_list[func] = root_package


for func, m in func_list.items():
    signature = inspect.signature(m.execute)
    func_name = func.replace('.', '_').replace('_api', '')
    api = textwrap.dedent(f"""
        @app.{m.method}('{m.path}')
        {'async ' if m.is_async else ''}def api_of_{func_name}{str(signature).replace(func, 'm')}:
            return func_list['{func}'].execute({
                ', '.join(signature.parameters.keys())
            })
    """)
    print(api)
    exec(api)
