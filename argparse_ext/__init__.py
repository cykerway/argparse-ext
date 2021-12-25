#!/usr/bin/env python3

'''
argparse ext;
'''

from argparse import ONE_OR_MORE
from argparse import OPTIONAL
from argparse import PARSER
from argparse import REMAINDER
from argparse import ZERO_OR_MORE
from gettext import gettext as _
import argparse

class HelpFormatter(argparse.HelpFormatter):

    '''
    formatter for generating usage messages and argument help strings;

    improvements over super class:

    -   default indent increment is 4 (io: 2);

    -   default max help position is 48 (io: 24);

    -   short and long options are formatted together;

    -   do not list options in usage;

    -   do not wrap usage;

    -   enclose metavars of mandatory arguments in braces;

    -   do not format choices metavar;

    -   do not capitalize default optional metavar;
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
            args_string = self._format_args(action, default)
            if args_string:
                return args_string
            return ', '.join(self._metavar_formatter(action, default)(1))
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

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
#        elif action.choices is not None:
#            choice_strs = [str(choice) for choice in action.choices]
#            result = '%s' % ','.join(choice_strs)
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            else:
                return (result, ) * tuple_size
        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '{%s}' % get_metavar(1)
        elif action.nargs == OPTIONAL:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == ZERO_OR_MORE:
            result = '[%s [%s ...]]' % get_metavar(2)
        elif action.nargs == ONE_OR_MORE:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == REMAINDER:
            result = '...'
        elif action.nargs == PARSER:
            result = '%s ...' % get_metavar(1)
        else:
            formats = ['{%s}' for _ in range(action.nargs)]
            result = ' '.join(formats) % get_metavar(action.nargs)
        return result

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
                    optionals.append(action)
                else:
                    positionals.append(action)

            # build full usage string
            format = self._format_actions_usage
            action_usage = format(positionals, groups)
            usage = ' '.join([s for s in [
                prog, '[options]' if optionals else '', action_usage
            ] if s])

        # prefix with 'usage:'
        return '%s%s\n\n' % (prefix, usage)

    def _get_default_metavar_for_optional(self, action):
        return action.dest

#    def add_arguments(self, actions):
#        actions = sorted(actions, key=lambda x: x.option_strings[::-1])
#        super().add_arguments(actions)

class RawDescriptionHelpFormatter(HelpFormatter):

    '''
    retain any formatting in descriptions;
    '''

    def _fill_text(self, text, width, indent):
        return ''.join(indent + line for line in text.splitlines(keepends=True))

