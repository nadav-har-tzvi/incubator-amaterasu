"""
{amaterasu_logo}

Usage: ama <command> [<args>...]

Builtin commands:
    init        Start a new Amaterasu compliant repository
    update      Update an existing Amaterasu repository based on a maki file
    run         Run an Amaterasu pipeline

{additional_commands}

See 'ama <command> --help' for more detailed information.
"""
from amaterasu.cli.handlers.base import BaseHandler

__version__ = '0.2.0-incubating'

import colorama
import pkgutil
import importlib
import inspect
from docopt import docopt
from .cli import common, consts, handlers

colorama.init()
lines = []
for idx, line in enumerate(common.RESOURCES[consts.AMATERASU_LOGO]):
    if idx <= 7:
        lines.append("\033[38;5;202m" + line)
    elif 7 < idx < 14:
        lines.append("\033[38;5;214m" + line)
    else:
        lines.append("\033[38;5;220m" + line)
desc = ''.join(lines)
desc += colorama.Fore.RESET + '\n\n'
desc += common.RESOURCES[consts.APACHE_LOGO]
desc += common.RESOURCES[consts.AMATERASU_TXT]


def load_handlers():
    return {
        name.split('.')[-1]: importlib.import_module(name)
        for _, name, _
        in pkgutil.iter_modules(handlers.__path__, handlers.__name__ + ".")
        if not name.endswith('base')
    }

def extract_args(args):
    """
    Cleans docopt's output, collects the <arg> arguments, strips the "<" ">" and returns an equivalent dictionary
    :param args: docopt result arguments
    :type args: dict
    :return:
    """
    return {
        k.strip('<').strip('>'): v
        for k, v
        in args.items()
        if k.startswith('<')
    }

def find_handler(handler_module):
    """
    Looks for a handler class that inherits from BaseHandler. We assume that the class with the longest MRO is
    the one we look for
    :param handler_module: A handler module loaded by importlib
    :return:
    """
    members = inspect.getmembers(handler_module)
    handler_candidates = []
    for member_name, member_obj in members:
        if hasattr(member_obj, '__mro__') and BaseHandler in member_obj.__mro__:
            handler_candidates.append((member_obj, member_obj.__mro__))
    return max(handler_candidates, key=lambda c: len(c[1]))[0]



def main():
    doc = __doc__.format(amaterasu_logo=desc, additional_commands='')  # TODO: implement additional_commands
    root_args = docopt(doc, version=__version__, options_first=True)
    handlers = load_handlers()
    command = root_args['<command>']
    if command in handlers:
        handler_vars = vars(handlers[command])
        cmd_args = docopt(handler_vars['__doc__'], version=handler_vars.get('__version__', __version__))
        handler = find_handler(handlers[command])
        handler(**extract_args(cmd_args)).handle()
    else:
        print(doc)