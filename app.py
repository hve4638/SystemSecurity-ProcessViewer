import sys, os
from front_api import FrontAPI
from cli import RunAsCLI
from gui_2 import GUimain
try:
        #from gui_2 import GUimain
        pass
except ModuleNotFoundError:
        GUimain = lambda x : sys.stderr.write("GUI not support\n")

CLI_MODE:bool = False

if __name__ == "__main__":
        FrontAPI.initialize()
        if CLI_MODE:
                cli = RunAsCLI(FrontAPI)
                cli.main()
        else:
                GUimain(FrontAPI)
