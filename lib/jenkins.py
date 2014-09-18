#!/usr/bin/env python
#
# Take a tree of test results and process it, producing a set of html
# reports.
#

from os                                 import getenv, path
from sys                                import exit, argv
from logging                            import debug, error, basicConfig, DEBUG, WARNING
from lib._jenkins                       import Jenkins, JenkinsException, LAUNCHER_SSH, LAUNCHER_COMMAND, LAUNCHER_WINDOWS_SERVICE
import json
from lib.configuration                  import Configuration
from lib.log                            import cdebug

# Server
#
class Server():
    try:
        jenkins = Jenkins(Configuration['jenkins']['server_url'])
    except:
        print('')
        print('Error: The configuration file doesn\'t contain a jenkins server url. See the example config file')
        print('       in the kernel-testing source directory.')
        print('')

    # info
    #
    @classmethod
    def info(cls, args):
        print(json.dumps(cls.jenkins.get_info(), sort_keys=True, indent=4))

# Common
#
class Common():
    # __common
    #
    @classmethod
    def __common(cls, args):
        '''
        Each command needs to see if the url was specified on the command line
        and adjust the server instance accordingly.
        '''
        if args.url:
            cls.jenkins = Jenkins(args.url)

# Nodes
#
class Nodes(Common):
    jenkins = Server.jenkins

    # info
    #
    @classmethod
    def details(cls, args):
        cdebug('Enter: Nodes.details')
        retval = 0
        cls._Common__common(args)

        if len(args.nodes) > 0:
            for n in args.nodes:
                data = cls.jenkins.get_node_info(n)
        else:
            data = cls.jenkins.get_node_info()

        print(json.dumps(data, sort_keys=True, indent=4))

        cdebug('Leave: Nodes.details')
        return retval

    # lister
    #
    @classmethod
    def lister(cls, args):
        cdebug('Enter: Nodes.lister')
        retval = 0
        cls._Common__common(args)

        if len(args.nodes) == 0:
            data = cls.jenkins.get_node_info()['computer']
        else:
            data = []
            for n in args.nodes:
                data.append(cls.jenkins.get_node_info(n))

        if args.details:
            for n in data:
                if args.format:
                    print(args.format % n)
                else:
                    print('%(displayName)-60s %(offline)s %(idle)s' % n)
        else:
            for n in data:
                print(n['displayName'])
        cdebug('Leave: Nodes.lister')
        return retval

    # delete
    #
    @classmethod
    def delete(cls, args):
        cdebug('Enter: Nodes.delete')
        retval = 0
        cls._Common__common(args)

        for n in args.nodes:
            try:
                cls.jenkins.delete_node(n)

            except JenkinsException as e:
                print('node-delete: cannot delete \'%s\': The job does not exist.' % n)
                retval = 1

        cdebug('Leave: Nodes.delete')
        return retval

    # create
    #
    @classmethod
    def create(cls, args):
        cdebug('Enter: Nodes.create')
        retval = 0
        cls._Common__common(args)

        if args.launcher == 'ssh':
            launcher = LAUNCHER_SSH
        elif args.launcher == 'command':
            launcher = LAUNCHER_COMMAND
        elif args.launcher == 'windows-service':
            launcher = LAUNCHER_WINDOWS_SERVICE

        if args.params:
            launcher_params = json.loads(args.params)

        cls.jenkins.create_node(args.node[0],
                                labels=args.tags,
                                launcher=launcher, nodeDescription=args.description, launcher_params=launcher_params)

        cdebug('Leave: Nodes.create')
        return retval

# Jobs
#
class Jobs(Common):
    jenkins = Server.jenkins

    @classmethod
    def __exists(cls, name):
        '''
        Returns true/false based on whether the specified job name exists on the
        Jenkins server.
        '''
        retval = False
        data = cls.jenkins.get_info()['jobs']
        for j in data:
            if name == j['name']:
                retval = True
                break
        return retval

    # clone
    #
    @classmethod
    def clone(cls, args):
        cdebug('Enter: Jobs.clone')
        cdebug('    existing_job: %s' % args.existing_job)
        cdebug('       clone_job: %s' % args.clone_job)
        cdebug('       overwrite: %s' % args.overwrite)
        retval = 0
        cls._Common__common(args)
        try:
            if cls.jenkins.job_exists(args.clone_job) and not args.overwrite:
                print('job-clone: the job \'%s\' already exists and the overwrite option was not spcified.' % args.clone_job)
                retval = 1
            else:
                cls.jenkins.copy_job(args.existing_job, args.clone_job)
        except JenkinsException as e:
            if not cls.jenkins.job_exists(args.existing_job):
                print('job-clone: the job \'%s\' does not exit.' % args.existing_job)
                retval = 1

        cdebug('Leave: Jobs.clone')
        return retval

    # create
    #
    @classmethod
    def create(cls, args):
        cdebug('Enter: Jobs.create')
        retval = 0
        cls._Common__common(args)
        cdebug('Leave: Jobs.create')
        return retval

    # control
    #
    @classmethod
    def control(cls, args):
        cdebug('Enter: Jobs.control')
        retval = 0
        cls._Common__common(args)
        if args.enable:
            for j in args.jobs:
                try:
                    cls.jenkins.enable_job(j)
                except JenkinsException as e:
                    print('job-control: the job \'%s\' does not exist.' % j)
                    retval = 1
        elif args.disable:
            for j in args.jobs:
                try:
                    cls.jenkins.disable_job(j)
                except JenkinsException as e:
                    print('job-control: the job \'%s\' does not exist.' % j)
                    retval = 1
        cdebug('Leave: Jobs.control')
        return retval

    # start
    #
    # FIXME bjf : Unless '-q | --quiet' is specified, return the job # that was started
    #
    @classmethod
    def start(cls, args):
        '''
        '''
        cdebug('Enter: Jobs.start')
        retval = 0
        cls._Common__common(args)
        for j in args.jobs:
            try:
                cls.jenkins.build_job(j)

            except JenkinsException as e:
                print('job-start: cannot start \'%s\': The job does not exist.' % j)
                retval = 1

        cdebug('Leave: Jobs.start')
        return retval

    # stop
    #
    @classmethod
    def stop(cls, args):
        '''
        '''
        cdebug('Enter: Jobs.stop')
        retval = 0
        cls._Common__common(args)
        for j in args.jobs:
            try:
                cls.jenkins.stop_build(j)

            except JenkinsException as e:
                print('job-stop: cannot stop \'%s\': The job does not exist.' % j)
                retval = 1

        cdebug('Leave: Jobs.stop')
        return retval

    # delete
    #
    @classmethod
    def delete(cls, args):
        '''
        Delete one or more jobs from the Jenkins server.
        '''
        cdebug('Enter: Jobs.delete')
        retval = 0
        cls._Common__common(args)
        for j in args.jobs:
            try:
                cls.jenkins.delete_job(j)

            except JenkinsException as e:
                print('job-delete: cannot delete \'%s\': The job does not exist.' % j)
                retval = 1

        cdebug('Leave: Jobs.delete')
        return retval

    # lister
    #
    @classmethod
    def lister(cls, args):
        cdebug('Enter: Jobs.lister')
        retval = 0
        cls._Common__common(args)
        data = cls.jenkins.get_info()['jobs']
        if len(args.jobs) > 0:
            tmp = []
            for j in data:
                if j['name'] in args.jobs:
                    tmp.append(j)
                data = tmp

        if args.details:
            for j in data:
                print('%(name)-60s %(color)7s %(url)s' % j)
        if args.info:
            for j in data:
                print(cls.jenkins.get_job_config(j['name']).replace('  ', '    '))
        else:
            for j in data:
                print(j['name'])
        cdebug('Leave: Jobs.lister')
        return retval

