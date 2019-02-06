#!/usr/local/bin/python

import setup_tests
from nose import with_setup
from nose.tools import nottest
from logging_decorator import logging

class TestActionableDict():

    @classmethod
    def setup_class(self):
        pass

    @logging
    @nottest
    def example_method(self, a, b):
        print("this is a test")

    def test_can_instantiate_class(self):
        self.example_method("alpha", "beta")

