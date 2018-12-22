class ActionableDict(dict):

    parent = None

    def __init__(self, initial_dict, parent = None):
        self.parent = parent
        for key, value in initial_dict.items():
            if isinstance(value, dict):
                initial_dict[key] = ActionableDict(value, self)
        super(ActionableDict, self).__init__(initial_dict)

    def __setitem__(self, item, value):
        if isinstance(value, dict):
            _value = ActionableDict(value, self)
        else:
            _value = value
        #print("You are changing the value of {} to {}!!".format(item, _value))
        self._traverse_parents()
        super(ActionableDict, self).__setitem__(item, _value)

    def _traverse_parents(self):
        test_item = self
        parent_keys = [ next(iter(self)) ]
        while(hasattr(test_item, 'parent') and test_item.parent != None):
            for key, value in test_item.parent.items():
                if value == test_item:
                    parent_keys.append(key)
            test_item = test_item.parent
        #print("parent keys: " + str(parent_keys[::-1]))
