from front_api import FrontAPI
<<<<<<< HEAD
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
=======
from gui_2 import GUimain

if __name__ == "__main__":
        GUimain(FrontAPI)
        pass
>>>>>>> e5235519ab99ca0d4bd297899a719dc0e69c6dc0
