#from .reg import *
#from .check01 import check_pc01, check_pc02
from os import *
import subprocess
from .check01 import check_pc01, check_pc02, check_pc03, check_pc04, check_pc05, check_pc16, check_pc15
from .check02 import check_pc10, check_pc11, check_pc12, check_pc13, check_pc19
from .check03 import check_pc06, check_pc07, check_pc08, check_pc09
from .check17 import check_pc17
from .check18 import check_pc18
from .solve01 import solve_pc01, solve_pc02, solve_pc03, solve_pc04, solve_pc05, solve_pc06, solve_pc15, solve_pc16
from .solve02 import solve_pc10, solve_pc11, solve_pc12, solve_pc13, solve_pc19
from .solve03 import solve_pc06, solve_pc07, solve_pc09
from .solve03 import solve_pc08_A, solve_pc08_B

def solve_pc08():
    solve_pc08_A()
    solve_pc08_B()


def __noneused():
    check_pc01()
    check_pc02()
    check_pc03()
    check_pc04()
    check_pc05()
    check_pc06()
    check_pc07()
    check_pc08()
    check_pc09()
    check_pc10()
    check_pc11()
    check_pc12()
    check_pc13()
    # check_pc14()
    check_pc15()
    check_pc16()
    check_pc17()
    check_pc18()
    check_pc19()

def __noneused2():
    solve_pc01()
    solve_pc02()
    solve_pc03()
    solve_pc04()
    solve_pc05()
    solve_pc06()
    solve_pc07()
    solve_pc08()
    solve_pc09()
    solve_pc10()
    solve_pc11()
    solve_pc12()
    solve_pc13()
    # solve_pc14()
    solve_pc15()
    solve_pc16()
    solve_pc17()
    solve_pc18()
    solve_pc19()
