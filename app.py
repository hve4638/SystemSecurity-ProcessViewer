import sys, os
from front_api import FrontAPI
from gui_2 import GUimain


if __name__ == "__main__":
        FrontAPI.initialize()
        
        GUimain(FrontAPI)
        pass
