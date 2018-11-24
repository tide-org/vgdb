import sys
sys.path.append("..")

from filter_predicate_base import filter_predicate_base

class vg_breakpoints(filter_predicate_base):

    @property
    def line_matchers(self):
        return [
            {
                'vg_name': 'vg_breakpoints',
                'regex': '(0x[0-9a-f]{2,16})',
                'type': 'array',
                'description': 'match each address in the breakpoints output and place in an array'
            },
        ]
