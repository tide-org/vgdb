#!/usr/local/bin/python

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

from nose import with_setup
from actionable_dict import ActionableDict

class TestActionableDict():

    @classmethod
    def setup_class(self):
        pass

    def test_can_add_to_dict(self):
        test_dict = ActionableDict( { 'b': { 'c': 3 } })
        assert test_dict['b']['c'] == 3
