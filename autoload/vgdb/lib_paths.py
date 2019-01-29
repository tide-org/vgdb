import sys
import os
import inspect

lib_paths = [
                'ptyprocess',
                'pexpect',
                'pyyaml/lib3',
                'jinja',
                'markupsafe/src',
                'yamlreader/src/main/python'
            ]

lib_base_path = "../lib"
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

for lib_path in lib_paths:
    lib_dir = os.path.join(currentdir, lib_base_path, lib_path)
    sys.path.insert(0, lib_dir)
