#!/usr/bin/env python
#

from sys                                import stdout
from subprocess                         import Popen, PIPE
from threading                          import Thread
from time                               import sleep

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

# ShellTimeoutError
#
class ShellTimeoutError(Exception):
    """
    """
    def __init__(self, cmd, timeout):
        self.__cmd = cmd
        self.__timeout = timeout

    @property
    def cmd(self):
        '''
        The shell command that was being executed when the timeout occured.
        '''
        return self.__cmd

    @property
    def timeout(self):
        '''
        The timeout period that expired.
        '''
        return self.__timeout

# ShellError
#
class ShellError(Exception):
    """
    """
    def __init__(self, cmd, returncode):
        self.__cmd = cmd
        self.__returncode = returncode

    @property
    def cmd(self):
        '''
        The shell command that was executed and returned a non-zero exit status.
        '''
        return self.__cmd

    @property
    def returncode(self):
        '''
        The exit status value for the command that was executed.
        '''
        return self.__returncode

# enqueue_output
#
def enqueue_output(out, queue, quiet=False):
    for line in iter(out.readline, b''):
        queue.put(line)
        if not quiet:
            stdout.write(line)
            stdout.flush()
    out.close()

# sh
#
def sh(cmd, timeout=None, ignore_result=False, quiet=False):
    out = []
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=1, shell=True)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q, quiet))
    t.daemon = True # thread dies with the program
    t.start()

    if timeout is not None:
        t.join(timeout)
        if t.is_alive():
            p.terminate()
            raise ShellTimeoutError(cmd, timeout)

    # ... do other things here

    while p.poll() is None:
        # read line without blocking
        try:
            line = q.get_nowait() # or q.get(timeout=.1)
        except Empty:
            pass
            #print('no output yet')
        else: # got line
            out.append(line)
        sleep(1)
    try:
        line = q.get_nowait() # or q.get(timeout=.1)
    except Empty:
        pass
        #print('no output yet')
    else: # got line
        out.append(line)

    if not ignore_result:
        if p.returncode != 0:
            raise ShellError(cmd, p.returncode)

    return p.returncode, out

# vi:set ts=4 sw=4 expandtab syntax=python:
