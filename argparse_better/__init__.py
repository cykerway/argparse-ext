#!/usr/bin/env python3

'''
module `argparse_better`;
'''

from gettext import gettext as _
import argparse

class HelpFormatter(argparse.HelpFormatter):

    '''
    formatter for generating usage messages and argument help strings;

    difference from super class:

    -   default indent increment is 4 (io: 2);

    -   default max help position is 48 (io: 24);

    -   short and long options are formatted together;

    -   actions are sorted by long option strings;

    -   omit options in usage and not wrap usage;
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

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = _('usage: ')

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)

        # if optionals and positionals are available, calculate usage
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)

            # split optionals from positionals
            optionals = []
            positionals = []
            for action in actions:
                if action.option_strings:
                    pass
                else:
                    positionals.append(action)

            # build full usage string
            format = self._format_actions_usage
            action_usage = format(optionals + positionals, groups)
            usage = ' '.join([s for s in [prog, action_usage] if s])

        # prefix with 'usage:'
        return '%s%s\n\n' % (prefix, usage)

    def add_arguments(self, actions):
        actions = sorted(actions, key=lambda x: x.option_strings[::-1])
        super().add_arguments(actions)

