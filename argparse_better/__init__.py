#!/usr/bin/env python3

'''
module `argparse_better`;
'''

import argparse

class HelpFormatter(argparse.HelpFormatter):

    '''
    formatter for generating usage messages and argument help strings;

    difference from super class:

    -   default indent increment is 4 (io: 2);

    -   default max help position is 48 (io: 24);

    -   short and long options are formatted together;

    -   actions are sorted by long option strings;
    '''

    def __init__(self, prog, indent_increment=4, max_help_position=48,
                 width=None):
        return super().__init__(
            prog=prog,
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
        )

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            if action.nargs == 0:
                return '{}{}'.format(
                    ' ' * 4 * int(action.option_strings[0].startswith('--')),
                    ', '.join(action.option_strings),
                )
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                return '{}{}'.format(
                    ' ' * 4 * int(action.option_strings[0].startswith('--')),
                    ', '.join(action.option_strings),
                ) + ' ' + args_string

    def add_arguments(self, actions):
        actions = sorted(actions, key=lambda x: x.option_strings[::-1])
        super().add_arguments(actions)

