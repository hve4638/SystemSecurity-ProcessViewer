from typing import Final
from front_api import FrontAPI
from gui import FileExplorer
from cli import RunAsCLI

CIL_MODE:Final = True

if __name__ == "__main__":
    if CIL_MODE:
        # GUI에서도 FrontAPI를 인자로 받아 사용합니다
        cli = RunAsCLI(FrontAPI)
        exit(cli.main())
        pass

    #print(FileExplorer)