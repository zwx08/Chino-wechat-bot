from time import sleep
from func_timeout import func_set_timeout
import eventlet

def main():
    eventlet.monkey_patch()
    with eventlet.Timeout(3,False):
        an = str(eval("9**9**9"))
main()