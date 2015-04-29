
from __future__ import print_function
from collections import OrderedDict
from functools import wraps

COMMANDS = OrderedDict()

def makeCommand(desc, namelist):
    def _command(f):
        @wraps(f)
        def _wrapper(*args, **kargs):
            return f(*args, **kargs)

        if isinstance(namelist, list):
            for n in namelist:
                COMMANDS[n] = (f,desc)
        else:
            COMMANDS[namelist] = (f, desc)
        return _wrapper

    return _command

def printCmdList():
    for name, info in COMMANDS.iteritems():
        print("{0:20} | {1}".format(name, info[1]))

def printCmdInfo(cmdname):
    cmdinfo = COMMANDS[cmdname]
    print("Command: [{0}]".format(cmdname))
    print(cmdinfo[0].__doc__)

def executeCommand(cmdname, args):
    try:
        cmdinfo = COMMANDS[cmdname]
        status = cmdinfo[0](args)
        return status
    except KeyError, fault:
        print("KeyError:", str(fault))
        help([cmdname])
        return False



@makeCommand('Prints help', 'help')
def help(args):
    if args is None:
        print("Usage: unitz <command> [args]")
        print("<command>: The command which needs to run.")
        print("[args]: Zero or more args. This varies according commands\n")
        print("Need more details? help commands take arguments, run: unitz help help")
        return False
    else:
        if len(args) > 0:
            cmdname = args[0]
            if cmdname == 'help':
                print("help command takes the following options:")
                print("help help       Prints this help")
                print("help all        Lists all available commands")
                print("help <command>  Gives more details about the <command>")
            elif cmdname == 'all':
                print("List of available commands. Usage: unitz <command> [args]")
                printCmdList()
            else:
                try:
                    printCmdInfo(cmdname)
                except KeyError:
                    print("Error: not such command [{0}]".format(cmdname))
                    return False
    return True


@makeCommand('Runs a flow', 'run')
def runFlow(args):
    """run <config> <flow name> [flow args]
<config>     The name of the configuration
<flow name>  The name of the flow
[flow args]  Zero or more arguments to the flow. This varies from flow to flow
"""
    if args is None or len(args) < 2:
        print("Error: not enough arguments")
        print(runFlow.__doc__.splitlines()[0])
        return False

    import unitz.tools
    unitz.tools.runFlow(args)

    return True

@makeCommand('Shows available units in a config', 'listu')
def listUnits(args):
    """listu <config> <flow name> [flow args]
<config>     The name of the configuration
"""
    if args is None or len(args) < 1:
        print("Error: not enough arguments")
        print(listUnits.__doc__.splitlines()[0])
        return False

    import unitz.tools
    unitz.tools.listUnits(args)

    return True

@makeCommand('Shows available flows in a config', 'listf')
def listFlows(args):
    """listf <config> <flow name> [flow args]
<config>     The name of the configuration
"""
    if args is None or len(args) < 1:
        print("Error: not enough arguments")
        print(listFlows.__doc__.splitlines()[0])
        return False

    import unitz.tools
    unitz.tools.listFlows(args)

    return True



