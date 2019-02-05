import os

def get_vgdb_base_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    join_paths = script_dir, "..", ".."
    return os.path.join(*join_paths)
