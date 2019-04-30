import os
import re
import sys


class ImportDir(object):
    def __init__(self, path):
        self.root_path = path
        self.__module_file_regexp__ = r'(.+)\.py(c?)$'
        self.__ignored_dirs_regexp__ = r'(^(\_|\.)|\_$)'
        self.module_names = set()

    def __get_module_names_in_dir__(self, path):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            regexp_result = re.search(self.__module_file_regexp__, entry)
            if os.path.isfile(full_path) and regexp_result:
                root_dirs = self.root_path.split(os.path.sep)
                path_dirs = full_path.split(os.path.sep)
                path_token = [str(d) for d in path_dirs if d not in root_dirs and str(d) != entry]
                path_token.append(regexp_result.groups()[0])
                module_name = '.'.join(path_token)
                self.module_names.add(module_name)
            elif os.path.isdir(full_path) and not re.search(self.__ignored_dirs_regexp__, entry):
                self.__get_module_names_in_dir__(full_path)

    def do(self, *, whitelist=None, blacklist=None, judge=None):
        env = dict()
        self.module_names.clear()
        self.__get_module_names_in_dir__(self.root_path)
        sys.path.append(self.root_path)
        module_names = [
            m for m in self.module_names
            if (whitelist is None or m in whitelist) and
               (blacklist is None or m not in blacklist) and
               (judge is None or judge(m))
        ]
        for module_name in module_names:
            root_package = module_name.split('.')[0]
            env[root_package] = __import__(module_name)
        return env, module_names
