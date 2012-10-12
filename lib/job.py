#!/usr/bin/env python
#
from sys                                import stdout
from subprocess                         import Popen, STDOUT, PIPE
from threading                          import Thread
from logging                            import debug

class Command(object):
    '''
    Enables to run subprocess commands in a different thread
    with TIMEOUT option!

    Based on jcollado's solution:
    http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    '''
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=None, **kwargs):
        def target(**kwargs):
            self.process = Popen(self.cmd, **kwargs)
            self.stdout, self.stderr = self.process.communicate()

        thread = Thread(target=target, kwargs=kwargs)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()

        return self.process.returncode, self.stdout, self.stderr

def sh2(cmd, timeout=None, quiet=False, ignore_result=False):
    command = Command(cmd)
    if not quiet:
        debug('sh2: \'%s\'' % cmd)
    status, std_out, std_err = command.run(timeout=timeout, shell=True, stderr=STDOUT, stdout=PIPE)
    if not quiet:
        debug('sh2 status: %d' % status)
    return status, std_out

def sh(cmd, timeout=None, quiet=False, ignore_result=False):
    command = Command(cmd)
    if not quiet:
        debug('sh: \'%s\'' % cmd)
    status = command.run(timeout=timeout, shell=True)[0]
    if not quiet:
        debug('sh status: %d' % status)
    return status

if __name__ == '__main__':
    command = Command("for i in 1 2 3 4 5; do echo \"hello\"; sleep 10; done")
    command.run(shell=True)
