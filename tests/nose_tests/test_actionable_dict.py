#!/usr/local/bin/python

import setup_tests
from nose import with_setup
from nose.tools import nottest
from actionable_dict import ActionableDict

@nottest
def callback_test(parent_dict, value):
    print("value changed: " + str(value) + " with keys: " + str(parent_dict))

class TestActionableDict():

    @classmethod
    def setup_class(self):
        pass

    def test_can_add_to_dict(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } } )
        self.test_dict['b']['c'] = 6
        assert self.test_dict['b']['c'] == 6

    def test_can_set_callback(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, callback_test)
        assert self.test_dict.callback != None

    def test_can_call_callback(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, callback_test)
        self.test_dict['b']['c'] = 5
        assert self.test_dict.callback != None


