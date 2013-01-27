#!/usr/bin/env python
#

from sys                                import stdout
from subprocess                         import Popen, PIPE, STDOUT
from threading                          import Thread
from time                               import sleep
from logging                            import debug, error, info, basicConfig, INFO, DEBUG, WARNING, getLevelName

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
    def __init__(self, cmd, returncode, output):
        self.__cmd = cmd
        self.__output = output
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

    @property
    def output(self):
        return self.__output

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
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, shell=True)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q, quiet))
    t.daemon = True # thread dies with the program
    t.start()

    if timeout is not None:
        t.join(timeout)
        if t.is_alive():
            p.terminate()
            raise ShellTimeoutError(cmd, timeout)

    while p.poll() is None:
        # read line without blocking
        try:
            line = q.get_nowait()
        except Empty:
            pass
        else: # got line
            out.append(line)
        sleep(1)

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            break
        else: # got line
            out.append(line)

    if not ignore_result:
        if p.returncode != 0:
            raise ShellError(cmd, p.returncode, out)

    return p.returncode, out

# ssh
#
def ssh(target, cmd, quiet=False, ignore_result=False):
    result, output = Shell.ssh(target, cmd, quiet=quiet, ignore_result=ignore_result)
    return result, output

class Shell():
    _dry_run = False

    def __init__(self):
        Shell._dry_run = False

    # ssh
    #
    @classmethod
    def ssh(cls, target, cmd, quiet=False, ignore_result=False):
        ssh_cmd = 'ssh %s %s' % (target, cmd)
        result = 0
        output = ''
        #print("ssh: '%s'" % ssh_cmd)
        if cls._dry_run:
            debug('[dry-run] %s' % (ssh_cmd))
        else:
            if not quiet:
                info(ssh_cmd)

            try:
                result, output = sh(ssh_cmd, quiet=quiet, ignore_result=ignore_result)

            except ShellError as e:
                if result != 0 and not ignore_result:
                    # Wait for just a few seconds and try it again.
                    #
                    #print(" **")
                    #print(" ** retrying the last command")
                    #print(" **")
                    result, output = sh(ssh_cmd, quiet=quiet, ignore_result=ignore_result)
                    if result != 0 and not ignore_result:
                        sleep(15)
                        raise ShellError(ssh_cmd, result, output)

        return result, output

# vi:set ts=4 sw=4 expandtab syntax=python:
