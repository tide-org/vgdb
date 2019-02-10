#!/usr/local/bin/python

from nose.tools import nottest
from logging_decorator import logging
import os

class TestActionableDict():

    _log_file_location = '/tests/vgdb_debug.log'

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(self._log_file_location):
            os.remove(self._log_file_location)

    @logging
    @nottest
    def example_method(self, a, b):
        "this is a test"

    def test_can_create_file(self):
        self.example_method("alpha", "beta")
        log_file_exists = os.path.isfile(self._log_file_location)
        assert log_file_exists == True

    def test_file_has_two_lines(self):
        self.example_method("alpha", "beta")
        num_lines = sum(1 for line in open(self._log_file_location))
        assert num_lines == 2

    def test_file_has_start_line(self):
        match = False
        self.example_method("alpha", "beta")
        for line in open(self._log_file_location):
            if "START" in line:
                match = True
        assert match == True

    def test_file_has_end_line(self):
        match = False
        self.example_method("alpha", "beta")
        for line in open(self._log_file_location):
            if "END" in line:
                match = True
        assert match == True
