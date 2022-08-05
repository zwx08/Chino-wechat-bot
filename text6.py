from inspect import getframeinfo, stack
import os
import sys


def main():
    #back_frame = sys._getframe().f_back
    #back_filename = os.path.basename(back_frame.f_code.co_filename)
    #print(back_filename)
    print(os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0])
class main2():
    def _3():
        main()
main2._3()