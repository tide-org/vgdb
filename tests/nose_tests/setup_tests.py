import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
vgdb_dir = os.path.join(current_dir, "../../autoload/vgdb")
vgdb_actions_dir = os.path.join(vgdb_dir, "./actions")
vgdb_filters_dir = os.path.join(vgdb_dir, "./filters")
vgdb_functions_dir = os.path.join(vgdb_dir, "./functions")
sys.path.insert(0, current_dir)
sys.path.insert(0, vgdb_dir)
sys.path.insert(0, vgdb_actions_dir)
sys.path.insert(0, vgdb_filters_dir)
sys.path.insert(0, vgdb_functions_dir)
import lib_paths
