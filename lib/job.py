#!/usr/bin/env python
#
from sys                                import stdout
from subprocess                         import Popen, STDOUT, PIPE
from threading                          import Thread

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

def sh(cmd, timeout=None):
    command = Command(cmd)
    return command.run(timeout=timeout, shell=True, stderr=STDOUT, stdout=PIPE)

