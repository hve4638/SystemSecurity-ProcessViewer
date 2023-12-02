import sys, os
from front_api import FrontAPI
from cli import RunAsCLI
try:
        from gui_2 import GUimain
except ModuleNotFoundError:
        GUimain = lambda x : sys.stderr.write("GUI not support\n")

CLI_MODE:bool = True

if __name__ == "__main__":
        FrontAPI.initialize()
        if CLI_MODE:
                cli = RunAsCLI(FrontAPI)
                cli.main()
        else:
                GUimain(FrontAPI)
