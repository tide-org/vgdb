#!/usr/local/bin/python

import setup_tests
from nose import with_setup
from nose.tools import nottest
from actionable_dict import ActionableDict

parent_keys_result = None

class TestActionableDict():

    @classmethod
    def setup_class(self):
        pass

    def test_can_add_to_dict(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } } )
        self.test_dict['b']['c'] = 6
        assert self.test_dict['b']['c'] == 6

    @staticmethod
    @nottest
    def callback_test_empty(parent_keys, value):
        pass

    @staticmethod
    @nottest
    def callback_test_parent_keys(parent_keys, value):
        parent_keys_result = parent_keys
        print("value changed: " + str(value) + " with keys: " + str(parent_keys))
        assert parent_keys != None

    @staticmethod
    @nottest
    def callback_test_value(parent_keys, value):
        parent_keys_result = parent_keys
        print("value changed: " + str(value) + " with keys: " + str(parent_keys))
        assert value != None

    @staticmethod
    @nottest
    def callback_test_parent_keys_correct(parent_keys, value):
        parent_keys_result = parent_keys
        print("value changed: " + str(value) + " with keys: " + str(parent_keys))
        assert parent_keys == ['b', 'c']

    @staticmethod
    @nottest
    def callback_test_value_correct(parent_keys, value):
        parent_keys_result = parent_keys
        print("value changed: " + str(value) + " with keys: " + str(parent_keys))
        assert value == 5

    def test_can_set_callback(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, self.callback_test_empty)
        assert self.test_dict.callback != None

    def test_can_call_callback_and_get_parent_keys(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, self.callback_test_parent_keys)
        self.test_dict['b']['c'] = 5

    def test_can_call_callback_and_get_value(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, self.callback_test_value)
        self.test_dict['b']['c'] = 5

    def test_can_call_callback_and_get_parent_keys_correct(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, self.callback_test_parent_keys_correct)
        self.test_dict['b']['c'] = 5

    def test_can_call_callback_and_get_value_correct(self):
        self.test_dict = ActionableDict( { 'b': { 'c': 3 } }, self.callback_test_value_correct)
        self.test_dict['b']['c'] = 5
