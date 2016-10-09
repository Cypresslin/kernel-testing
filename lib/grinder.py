#!/usr/bin/env python
#

from os                                 import path, makedirs, listdir, walk
from sys                                import argv
from shutil                             import rmtree, copytree, copyfile
from decimal                            import Decimal
import json

from mako.template                      import Template
from mako.exceptions                    import RichTraceback

from lib.utils                          import json_load, file_load, FileDoesntExist, string_to_date
from lib.log                            import center, cleave, cdebug

# o2ascii
#
# Convert a unicode string or a decial.Decimal object to a str.
#
def o2ascii(obj):
    retval = None
    if type(obj) != str:
        if type(obj) == unicode:
            retval = obj.encode('ascii', 'ignore')
        elif type(obj) == Decimal:
            retval = str(obj)
        elif type(obj) == int:
            retval = str(obj)
    else:
            retval = obj
    return retval

# locate
#
def locate(file_name):
    retval = None

    # Find it ...
    #
    fid = file_name
    if path.exists(fid): # Current directory
        retval = fid
    else:
        fid = path.join(path.dirname(argv[0]), file_name)
        if path.exists(fid):
            retval = fid

    return retval

# load_template
#
def load_template(file_name):
    """
    Load the template file.
    """
    retval = None

    # Find it ...
    #
    fid = file_name
    if not path.exists(fid): # Current directory
        fid = path.join(path.dirname(argv[0]), file_name)
        if not path.exists(fid):
            fid = None

    if fid is not None:
        with open(fid, 'r') as f:
            retval = f.read()
    else:
        print("Error: Failed to find the template file.")

    return retval

# CmdlineError
#
# The type of exception that will be raised by Cmdline.process() if there
# are command line processing errors.
#
class CmdlineError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

# Exit
#
class Exit():
    """
    If an error message has already been displayed and we want to just exit the app, this
    exception is raised.
    """
    pass

from xml.dom.minidom                    import Node, parseString
from lib.utils                          import dump

# x2dict
#
class x2dict(dict):

    # __init__
    #
    def __init__(self, xmlstring, *args):
        center("x2dict.__init__")

        dict.__init__(self, args)

        doc = parseString(xmlstring)

        x = self.e2d(doc)
        for k in x:
            self[k] = x[k]

        cleave("x2dict.__init__")

    # e2d
    #
    def e2d(self, node):
        center("x2dict.e2d")

        retval = None

        child = node.firstChild
        if not child:
            cdebug('No child nodes\n')
            cleave("x2dict.e2d")
            return None

        retval = {}
        text = ''
        while child is not None:
            if child.nodeType == Node.TEXT_NODE:
                cdebug('nodeType: Node.TEXT_NODE\n')
                cdebug('data: \'%s\'\n' % child.data.strip())
                text = child.data.strip()
                if text != '':
                    retval = { 'text' : text.split('\n') }
            elif child.nodeType == Node.ELEMENT_NODE:
                cdebug('tagName: %s\n' % child.tagName)
                cdebug('nodeType: Node.ELEMENT_NODE\n')

                if child.tagName not in retval:
                    cdebug('Creating retval[%s] list.\n' % (child.tagName))
                    retval[child.tagName] = []

                neo = self.e2d(child)
                if child.hasAttributes:
                    if neo is None:
                        neo = {}

                    for a in child.attributes.keys():
                        cdebug("attributes[%s] = %s\n" % (a, child.attributes[a].value))
                        neo[a] = child.attributes[a].value

                retval[child.tagName].append(neo)

            child = child.nextSibling

        cleave("x2dict.e2d")
        return retval

    # dump
    def dump(self):
        dump(self)

# JenkinsTestResultsTree
#
class JenkinsTestResultsTreeError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = "%s" % error

class JenkinsTestResultsTree(object):
    # __init__
    #
    def __init__(self, root):
        center("JenkinsTestResultsTree.__init__")

        self.root = root
        self.arkive = path.join(root, 'archive')

        cleave("JenkinsTestResultsTree.__init__")

    # results
    #
    @property
    def results(self):
        center("JenkinsTestResultsTree.results")

        retval = None
        try:
            content = file_load(path.join(self.root, 'junitResult.xml'))
            d = x2dict(content)

            # Convert to a more reasonable dictionary.
            #
            results = d['result'][0]

            r = {}
            r['duration'] = self.duration(results)
            r['keepLongStdio'] = self.text0(results['keepLongStdio'])
            r['suites'] = []

            for xx in results['suites'][0]['suite']:
                s = {}
                s['name'] = self.text0(xx['name'])
                s['duration'] = self.duration(xx)
                s['timestamp'] = self.text0(xx['timestamp'])
                s['file'] = self.text0(xx['file'])
                s['cases'] = []
                s['tests run'] = 0
                s['tests failed'] = 0
                s['tests skipped'] = 0

                for yy in xx['cases'][0]['case']:
                    c = {}

                    s['name'] = self.text0(yy['className'])
                    s['tests run'] += 1

                    c['name'] = self.text0(yy['testName'])
                    c['duration'] = self.duration(yy)
                    c['skipped'] = True if self.text0(yy['skipped']) == 'true' else False
                    if c['skipped']:
                        s['tests skipped'] += 1
                    c['failedSince'] = int(self.text0(yy['failedSince']))

                    try:
                        c['errorDetails'] = self.text(yy['errorDetails'])
                        s['tests failed'] += 1
                        c['errorStackTrace'] = self.text(yy['errorStackTrace'])

                    except KeyError:
                        pass

                    s['cases'].append(c)

                r['suites'].append(s)

            retval = r

        except FileDoesntExist as e:
            raise JenkinsTestResultsTreeError('The Jenkins test results tree (%s) specified on the command line does\n           not appear to be a valid results tree, the file (%s)\n           does not exist.\n' % (self.root, e.file_name))
            cleave("TestResultsRepository.__init__")

        cleave("JenkinsTestResultsTree.results")
        return retval

    @property
    def attributes(self):
        center("JenkinsTestResultsTree.attributes")

        retval = None
        try:
            retval = json_load(path.join(self.arkive, 'test-attributes.json'))

        except FileDoesntExist as e:
            raise JenkinsTestResultsTreeError('The Jenkins test results tree (%s) specified on the command line does\n           not appear to be a valid results tree, the file (%s)\n           does not exist.\n' % (self.root, e.file_name))
            cleave("TestResultsRepository.__init__")

        cleave("JenkinsTestResultsTree.attributes")
        return retval

    @property
    def archive(self):
        center("JenkinsTestResultsTree.archive")
        retval = path.join(self.root, 'archive')
        cleave("JenkinsTestResultsTree.archive")
        return retval

    # duration
    #
    def duration(self, d):
        retval = int(float(d['duration'][0]['text'][0]))
        return retval

    def text0(self, l):
        return l[0]['text'][0]

    def text(self, l):
        return l[0]['text']

# TestResultsRepository
#
class TestResultsRepositoryError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = "%s" % error

class TestResultsRepository():
    # __init__
    #
    def __init__(self, rc = 'test-results.rc'):
        '''
        Load the test-results.rc file into self.
        '''
        center("TestResultsRepository.__init__")

        try:
            # Find it ...
            #
            fid = rc
            if not path.exists(fid): # Current directory
                fid = path.join(path.expanduser('~'), rc)
                if not path.exists(fid): # Users home directory
                    fid = path.join(path.dirname(argv[0]), rc)
                    if not path.exists(fid):
                        fid = path.join(path.dirname(argv[0]), 'lib', rc)
                        if not path.exists(fid):
                            raise FileDoesntExist(rc)

            self.cfg = json_load(fid)

        except FileDoesntExist as e:
            raise TestResultsRepositoryError('The file (%s) does not exist.\n' % e.file_name)
            cleave("TestResultsRepository.__init__")

        cleave("TestResultsRepository.__init__")

    # initialize_results_dir
    #
    def initialize_results_dir(self, dirname):
        center("TestResultsRepository.initialize_results_dir")

        self.results_dir = path.join(self.cfg['repository_root'], dirname)
        if path.exists(self.results_dir):
            cdebug("%s exists.\n" % (self.results_dir))
            rmtree(self.results_dir)
        else:
            cdebug("%s does not exist.\n" % (self.results_dir))
        makedirs(self.results_dir)
        cleave("TestResultsRepository.initialize_results_dir")
        return self.results_dir

    def store_results(self, data):
        center("TestResultsRepository.store_results")

        destdir = path.join(self.results_dir, 'results.json')
        cdebug('destdir: "%s"' % destdir)
        with open(destdir, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4))

        cleave("TestResultsRepository.store_results")

    def ingest(self, jtr):
        center("TestResultsRepository.ingest")

        self.text_file_template = Template(filename=locate('text-file.mako'), default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf8')

        data = {}
        data['results'] = jtr.results
        attributes = data['attributes'] = jtr.attributes

        # Name of the directory where we will be storing the results
        #
        ts = string_to_date(attributes['timestamp']).strftime('%Y-%m-%d_%H-%M-%S')
        tr_dest = "%s/%s__%s__%s" % (attributes['kernel'], attributes['platform']['hostname'], attributes['kernel'], ts)
        dest = self.initialize_results_dir(tr_dest)
        for n in listdir(jtr.archive):
            if path.isdir(path.join(jtr.archive, n)):
                copytree(path.join(jtr.archive, n), path.join(dest, n))

        # Process "text" files to make them easier to read.
        #
        try:
            for root, dirs, files in walk(dest):
                for fid in files:
                    if fid.endswith('.DEBUG'):
                        with open(path.join(root, fid), 'r') as f:
                            content = f.read().split('\n')

                        d = path.join(root, '%s.html' % fid)
                        template = self.text_file_template.render(title = fid, content = content)
                        with open(d, 'w') as f:
                            f.write(template)

        except:
            traceback = RichTraceback()
            for (filename, lineno, function, line) in traceback.traceback:
                print("File %s, line %s, in %s" % (filename, lineno, function))
                print(line, "\n")
            print("%s: %s" % (str(traceback.error.__class__.__name__), traceback.error))

        if path.exists(path.join(jtr.root, 'log')):
            # There should always be a 'log' file which is the console log
            # of the job.
            #
            copyfile(path.join(jtr.root, 'log'), path.join(dest, 'console_output.txt'))

            fid = path.join(dest, 'console_output.txt')
            with open(fid, 'r') as f:
                content = f.read().split('\n')

            d = '%s.html' % fid
            template = self.text_file_template.render(title = fid, content = content)
            with open(d, 'w') as f:
                f.write(template)

        self.store_results(data)

        cleave("TestResultsRepository.ingest")

    @property
    def test_runs(self):
        center("TestResultsRepository.test_runs")
        retval = []
        for kver in listdir(self.cfg['repository_root']):
            p = path.join(self.cfg['repository_root'], kver)
            if path.isdir(p):
                for run in listdir(p):
                    p = path.join(self.cfg['repository_root'], kver, run)
                    if path.isdir(p):
                        retval.append(path.join(kver, run))
        cleave("TestResultsRepository.test_runs")
        return retval

    def results(self, test_run):
        center("TestResultsRepository.results")
        try:
            retval = json_load(path.join(self.cfg['repository_root'], test_run, 'results.json'))
        except FileDoesntExist as e:
            raise TestResultsRepositoryError('The file (%s) does not exist.\n' % e.file_name)
            cleave("TestResultsRepository.__init__")
        cleave("TestResultsRepository.results")
        return retval

# vi:set ts=4 sw=4 expandtab:

