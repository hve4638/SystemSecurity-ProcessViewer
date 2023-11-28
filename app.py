from typing import Final
from front_api import FrontAPI
# from gui import FileExplorer
from main.py import Guimain

CIL_MODE:Final = True

if __name__ == "__main__":
        Gui = Guimain(FrontAPI)
        exit(Gui.main())
        pass