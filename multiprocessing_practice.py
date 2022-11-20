from helper import Timer
from multiprocessing import Pool, Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    print('Starting id:', os.getpid())
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()