from typing import Final
from front_api import FrontAPI
from cli import RunAsCLI
# from gui import FileExplorer
#from main.py import Guimain

CLI_MODE:Final = True

if __name__ == "__main__":
        if CLI_MODE:
                cli = RunAsCLI(FrontAPI)
                exit(cli.main())
                pass
        else:
                Gui = Guimain(FrontAPI)
                exit(Gui.main())
                pass