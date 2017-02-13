#!/usr/bin/env python3
#

import os
import sys
import json
from time                               import sleep
from lib.exceptions                     import ErrorExit
from lib.log                            import center, cleave, cinfo, cdebug
from lib3.shell                         import sh, Shell, ShellError
from datetime                           import datetime

from simplestreams import filters
from simplestreams import mirrors
from simplestreams import util

FORMAT_JSON = "JSON"

from mako.template                      import Template
from jenkinsapi.jenkins                 import Jenkins
from lib3.jenkins_server_local          import JenkinsServerLocal

# CloudBase
#
class CloudBase(object):
    '''
    '''
    # __init__
    #
    def __init__(s):
        center(s.__class__.__name__ + '.__init__')
        s.target = None
        s.cloud  = None
        cleave(s.__class__.__name__ + '.__init__')

    # ssh
    #
    def ssh(s, cmd, additional_ssh_options='', quiet=True, ignore_result=False):
        '''
        This ssh method uses the lower-level ssh function for actuall remote shell to
        the target system. This helper automatically provides the 'target' and 'user'
        options to every ssh call.
        '''
        center("Base::ssh")
        # result, output = Shell.ssh(s.target, cmd, user='ubuntu', additional_ssh_options=additional_ssh_options, quiet=quiet, ignore_result=ignore_result)
        result, output = Shell.ssh(s.target, cmd, user=s.ssh_user, additional_ssh_options=additional_ssh_options, quiet=quiet, ignore_result=ignore_result)
        cleave("Base::ssh")
        return result, output

    # wait_for_target
    #
    def wait_for_target(s, timeout=30):
        '''
        Wait for the remote system to come up far enough that we can start talking
        (ssh) to it.
        '''
        center('Base::wait_for_system_ex')

        start = datetime.utcnow()
        cinfo('Starting waiting for \'%s\' at %s' % (s.target, start))

        # Keep spinning until we either timeout or we get back some output from 'uname -vr'
        #
        while True:
            try:
                if s.cloud == 'gce':
                    result, output = s.ssh('uname -vr', additional_ssh_options="-i ~/.ssh/google_compute_engine -o BatchMode=yes")
                else:
                    result, output = s.ssh('uname -vr', additional_ssh_options="-o BatchMode=yes")
                if result == 0 and len(output) > 0:
                    cdebug("exit result is 0")
                    break

            except ShellError as e:

                if 'port 22: Connection refused' in e.output:
                    # Just ignore this, we know that we can connect to the remote host
                    # otherwise we wouldn't have been able to reboot it.
                    #
                    print("** Encountered 'Connection refused'")
                    pass
                else:
                    print("Something else bad happened")
                    cleave('Base::wait_for_system')
                    raise

            now = datetime.utcnow()
            delta = now - start
            if delta.seconds > timeout * 60:
                cinfo('Timed out at: %s' % now)
                raise ErrorExit('The specified timeout (%d) was reached while waiting for the target system (%s) to come back up.' % (timeout, s.target))

            sleep(60)
            cinfo('Checking at: %s' % datetime.utcnow())

        cleave('Base::wait_for_system_ex')

# Cloud
#
class Cloud(object):
    '''
    '''
    # construct
    #
    @classmethod
    def construct(s, cloud):
        center(s.__class__.__name__ + '.construct')
        if cloud == 'aws':
            c = AWS()
        elif cloud == 'gce':
            c = GCE()
        elif cloud == 'azure':
            c = Azure()
        else:
            c = None
        cleave(s.__class__.__name__ + '.construct')
        return c

# Azure
#
class Azure(CloudBase):
    '''
    '''
    # __init__
    #
    def __init__(s):
        center(s.__class__.__name__ + '.__init__')
        CloudBase.__init__(s)
        s.cloud = 'azure'
        cleave(s.__class__.__name__ + '.__init__')

    def sh(s, cmd):
        command = 'azure vm ' + cmd
        r, o = sh(command, quiet=True)
        return r, o

    @property
    def ssh_options(s):
        return ''

    @property
    def ssh_user(s):
        return ''

    # list_instances
    #
    def list_instances(s):
        center(s.__class__.__name__ + '.list_instances')

        retval = {}
        result, output = s.sh('list --json')
        data = json.loads('\n'.join(output))
        for item in data:
            retval[item['VMName']] = {
                'external_ip' : item['Network']['Endpoints'][0]['virtualIPAddress'],
                'fqdn' : item['DNSName'],
                '__other__' : item,
            }

        cleave(s.__class__.__name__ + '.list_instances (%s)' % retval)
        return retval

    # fqdn
    #
    def fqdn(s, name):
        center(s.__class__.__name__ + '.fqdn')

        retval = None
        instances = s.list_instances()
        try:
            retval = instances[name]['fqdn']
        except:
            pass

        cleave(s.__class__.__name__ + '.fqdn (%s)' % retval)
        return retval

    # lookup_instance_ip
    #
    def lookup_instance_ip(s, name):
        center(s.__class__.__name__ + '.lookup_instance_ip')

        retval = None
        instances = s.list_instances()
        try:
            retval = instances[name]['external_ip']
        except:
            pass

        cleave(s.__class__.__name__ + '.lookup_instance_ip (%s)' % retval)
        return retval

    # create
    #
    def create(s, instance_name, series, region='West US'):
        center(s.__class__.__name__ + '.create')

        retval = 0
        s.instance_name = instance_name
        s.series = series

        images = CloudImages(s.cloud, series=series, region=region).images
        try:
            cmd = 'create %s %s jenkins --location "%s" --ssh --no-ssh-password --ssh-cert ~/.ssh/id_rsa.pub' % (s.instance_name, images[0]['id'], region)
            result, response = s.sh(cmd)
        except ShellError as e:
            retval = 1
            for l in e.output:
                l.strip()
                print(l)

        # if s.target is not None:
        #     s.wait_for_target()

        cleave(s.__class__.__name__ + '.create')
        return retval

    # destroy
    #
    def destroy(s, instance_name):
        center(s.__class__.__name__ + '.destroy')
        result, ourput = s.sh('delete --quiet --blob-delete %s' % (instance_name))
        cleave(s.__class__.__name__ + '.destroy')

# GCE
#
class GCE(CloudBase):
    '''
    '''
    # __init__
    #
    def __init__(s):
        center(s.__class__.__name__ + '.__init__')
        CloudBase.__init__(s)
        s.cloud = 'gce'
        cleave(s.__class__.__name__ + '.__init__')

    def sh(s, cmd):
        command = 'gcloud compute ' + cmd
        try:
            r, o = sh(command, quiet=True)
        except ShellError as e:
            for l in e.output:
                l.strip()
                print(l)
            raise
        return r, o

    @property
    def ssh_options(s):
        return '-i /var/lib/jenkins/.ssh/google_compute_engine'

    @property
    def ssh_user(s):
        return ''

    # list_instances
    #
    def list_instances(s):
        center(s.__class__.__name__ + '.list_instances')

        retval = {}
        result, response = s.sh('instances list')
        for l in response:
            if l.startswith('NAME'):
                continue
            fields = l.split()
            if len(fields) == 6:
                retval[fields[0]] = {
                    'zone'        : fields[1],
                    'type'        : fields[2],
                    'internal_ip' : fields[3],
                    'external_ip' : fields[4],
                    'status'      : fields[5],
                }
            elif len(fields) == 7:
                retval[fields[0]] = {
                    'zone'        : fields[1],
                    'type'        : fields[2],
                    'preemptible' : fields[3],
                    'internal_ip' : fields[4],
                    'external_ip' : fields[5],
                    'status'      : fields[6],
                }

        cleave(s.__class__.__name__ + '.list_instances (%s)' % retval)
        return retval

    # fqdn
    #
    def fqdn(s, name):
        center(s.__class__.__name__ + '.fqdn')

        retval = None
        instances = s.list_instances()
        try:
            retval = instances[name]['external_ip']
        except:
            pass

        cleave(s.__class__.__name__ + '.fqdn (%s)' % retval)
        return retval

    # lookup_instance_ip
    #
    def lookup_instance_ip(s, name):
        center(s.__class__.__name__ + '.lookup_instance_ip')

        retval = None
        instances = s.list_instances()
        try:
            retval = instances[name]['external_ip']
        except:
            pass

        cleave(s.__class__.__name__ + '.lookup_instance_ip (%s)' % retval)
        return retval

    @property
    def images(s):
        center(s.__class__.__name__ + '.images')
        retval = {}

        result, output = s.sh('images list')
        for line in output:
            if line.startswith('ubuntu'):
                fields = line.split()
                image = fields[0]

                fields = image.split('-')
                series = fields[2]

                retval[series] = image

        cleave(s.__class__.__name__ + '.images')
        return retval

    # create
    #
    # https://cloud.google.com/compute/docs/regions-zones/regions-zones
    #
    def create(s, instance_name, series, region='us-west1'):
        center(s.__class__.__name__ + '.create')
        cdebug('    instance_name: %s' % instance_name)
        cdebug('           series: %s' % series)
        cdebug('           region: %s' % region)
        retval = 0

        s.instance_name = instance_name
        s.series = series

        # r = '-'.join(region.split('-')[0:2])
        # images = CloudImages(s.cloud, series=series, region=r).images
        try:
            # print('image: %s' % (s.images[series]))
            # print('image: %s' % (images[0]['id']))
            # cmd = 'instances create %s --zone %s --network "default" --no-restart-on-failure --image-project ubuntu-os-cloud --image %s' % (s.instance_name, region, images[0]['id'].replace('daily-', ''))
            cmd = 'instances create %s --zone %s --network "default" --no-restart-on-failure --image-project ubuntu-os-cloud --image %s' % (s.instance_name, region, s.images[series])
            result, response = s.sh(cmd)
            for l in response:
                if l.startswith(s.instance_name):
                    fields = l.split()
                    s.target = fields[4]

            if s.target is not None:
                s.wait_for_target()
        except ShellError as e:
            retval = 1
            for l in e.output:
                l.strip()
                print(l)

        cleave(s.__class__.__name__ + '.create')
        return retval

    # destroy
    #
    def destroy(s, instance_name):
        center(s.__class__.__name__ + '.destroy')
        instances = s.list_instances()
        cmd = 'instances delete --quiet --zone %s %s' % (instances[instance_name]['zone'], instance_name)
        s.sh(cmd)
        cleave(s.__class__.__name__ + '.destroy')

# AWS
#
# aws ec2 describe-instances --filters "Name=tag:Name,Values=wanker"
#
class AWS(CloudBase):
    '''
    '''
    # __init__
    #
    def __init__(s):
        center(s.__class__.__name__ + '.__init__')
        CloudBase.__init__(s)
        s.cloud = 'aws'
        cleave(s.__class__.__name__ + '.__init__')

    def sh(s, cmd):
        retval = None
        r, o = sh('aws ec2 ' + cmd, quiet=True)
        try:
            retval = json.loads('\n'.join(o))
        except:
            pass
        return retval

    @property
    def ssh_options(s):
        return ''

    @property
    def ssh_user(s):
        return 'ubuntu'

    # list_instances
    #
    def list_instances(s):
        center(s.__class__.__name__ + '.list_instances')

        retval = {}
        response = s.sh('describe-instances --filters "Name=tag:Owner,Values=UbuntuKernelTeam"')

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'running':
                    continue
                tags = {}
                for t in instance['Tags']:
                    tags[t['Key']] = t['Value']

                try:
                    if tags['Owner'] == 'UbuntuKernelTeam':
                        retval[tags['Name']] = {
                            'instance_id' : instance['InstanceId'],
                            'status_code' : instance['State']['Code'],
                            'status_name' : instance['State']['Name'],
                        }
                        if 'PublicIpAddress' in instance:
                            retval[tags['Name']]['external_ip'] = instance['PublicIpAddress']
                        if 'PublicDnsName' in instance:
                            retval[tags['Name']]['fqdn'] = instance['PublicDnsName']
                        retval[tags['Name']]['__other__'] = instance

                except KeyError:
                    pass

        cleave(s.__class__.__name__ + '.list_instances (%s)' % retval)
        return retval

    # lookup_instance_ip
    #
    def lookup_instance_ip(s, name):
        center(s.__class__.__name__ + '.lookup_instance_ip')

        retval = None
        try:
            instances = s.list_instances()
            retval = instances[name]['external_ip']
        except:
            pass

        cleave(s.__class__.__name__ + '.lookup_instance_ip (%s)' % retval)
        return retval

    # fqdn
    #
    def fqdn(s, name):
        center(s.__class__.__name__ + '.fqdn')

        retval = None
        instances = s.list_instances()
        try:
            retval = instances[name]['fqdn']
        except:
            pass

        cleave(s.__class__.__name__ + '.fqdn (%s)' % retval)
        return retval

    @property
    def images(s):
        center(s.__class__.__name__ + '.images')
        retval = {}

        cleave(s.__class__.__name__ + '.images')
        return retval

    # create
    #
    def create(s, instance_name, series, region):
        center(s.__class__.__name__ + '.create')

        retval = 1
        ami = None

        # Note! If the series name is misspelled, we will get an "IndexError exception. We probably want
        #       to be smarter about that.

        images = CloudImages(s.cloud, series=series, region=region).images

        # Since we are just using t2.micro instances right now we are restricted to 'hvm' amis
        #
        # Instance comparison chart: http://www.ec2instances.info/
        #
        for image in images:
            if image['virt'] == 'hvm' and image['root_store'] == 'ssd':
                ami = image['id']
                break

        if ami is not None:
            cmd = 'run-instances --image-id %s --key-name cloud-figg --instance-type t2.micro --security-groups figg-security-group' % (ami)
            response = s.sh(cmd)
            reservation_id = response['ReservationId']

            response = s.sh('describe-instances')

            s.target    = None
            instance_id = None
            for reservation in response['Reservations']:
                if reservation['ReservationId'] == reservation_id:
                    try:
                        s.target = reservation['Instances'][0]['PublicIpAddress']
                        instance_id = reservation['Instances'][0]['InstanceId']
                        break
                    except:
                        print('ReservationId: %s' % reservation_id)
                        print(json.dumps(reservation, sort_keys=True, indent=4))

            s.sh('create-tags --resources %s --tags Key=Name,Value=%s' % (instance_id, instance_name))
            s.sh('create-tags --resources %s --tags Key=Owner,Value=UbuntuKernelTeam' % (instance_id))

            if s.target is not None:
                s.wait_for_target()
                retval = 0
        else:
            print('No AMIs found')

        cleave(s.__class__.__name__ + '.create')
        return retval

    # destroy
    #
    def destroy(s, instance_name):
        center(s.__class__.__name__ + '.destroy')
        instances = s.list_instances()
        if instance_name in instances:
            s.sh('terminate-instances --instance-ids %s' % instances[instance_name]['instance_id'])
        cleave(s.__class__.__name__ + '.destroy')

# CloudJobFactory
#
class CloudJobFactory(object):
    '''
    '''

    # __init__
    #
    def __init__(s, cloud, series, region, tests, request):
        '''
        '''
        center(s.__class__.__name__ + '.__init__')
        s.cloud  = cloud
        s.tests  = tests
        s.series = series
        s.region = region
        s.request = request
        s.jenkins = JenkinsServerLocal.connect()
        s.props_imported = False
        cleave(s.__class__.__name__ + '.__init__')

    def expand(s, collection):
        # By importing the TestCollections here, this way, we automatically
        # pick up changes to lib.tessprops without having to kill and restart
        # the utility (kmsgq-aws).
        #
        from lib.testsprops  import TestCollections
        s.props_imported = True

        result = []
        if collection in TestCollections:
            for test in TestCollections[collection]:
                for t in s.expand(test):
                    result.append(t)
        else:
            result.append(collection)
        return result

    # load_template
    #
    def load_template(s, file_name):
        """
        Load the template file.
        """
        center(s.__class__.__name__ + '.load_templace')
        retval = None

        if file_name[0] == '/' or file_name[0] == '.':
            # The full path is specified. Use the name as is.
            #
            fid = file_name
        else:
            # Find it ...
            #
            fid = file_name
            if not os.path.exists(fid):  # Current directory
                fid = os.path.join(os.path.dirname(sys.argv[0]), file_name)
                if not os.path.exists(fid):
                    fid = None

        if fid is not None:
            with open(fid, 'r') as f:
                retval = Template(f.read())
        else:
            print("Error: Failed to find the template file.")

        cleave(s.__class__.__name__ + '.load_templace')
        return retval

    # job_name
    #
    def job_name(s, test):
        center(s.__class__.__name__ + '.job_name')
        retval = s.cloud
        retval += '__'

        # The job name starts with some form of the test name(s)
        #
        retval += test
        retval += '__'

        retval += s.series

        cleave(s.__class__.__name__ + '.job_name (%s)' % retval)
        return retval

    def create_jobs(s):
        center(s.__class__.__name__ + '.create_jobs')
        retval = {}
        cl = Cloud.construct(s.cloud)
        tests = s.expand(s.tests)
        for test in tests:
            job_name = s.job_name(test)
            job_data = {
                'job_name'    : job_name,
                'series_name' : s.series,
                'cloud'       : s.cloud,
                'test'        : test,
                'region'      : s.region,
                'sut-name'    : job_name.replace('_', '-'),
                'ssh_options' : cl.ssh_options,
            }
            for k in s.request:
                job_data[k] = s.request[k]

            # The description is used by test-results-announce
            #
            job_data['description'] = json.dumps(job_data, sort_keys=True, indent=4)

            s.job_template = s.load_template('cloud-jenkins-test-job.mako')
            job_xml = s.job_template.render(data=job_data)

            try:
                s.jenkins.delete_job(job_name)
            except:
                pass

            s.jenkins.create_job(job_name, job_xml)

            # Separate out the buld_job
            #
            # sleep(10)
            # s.jenkins.build_job(job_name)
            retval[job_data['job_name']] = job_data
        cleave(s.__class__.__name__ + '.create_jobs')
        return retval

    def start_jobs(s, jobs):
        center(s.__class__.__name__ + '.create_jobs')
        for job in jobs:
            s.jenkins.build_job(job)
            sleep(2)

        cleave(s.__class__.__name__ + '.create_jobs')

    # main
    #
    def main(s):
        center(s.__class__.__name__ + '.main')
        retval = 0

        s.create_jobs()

        cleave(s.__class__.__name__ + '.main (%s)' % retval)
        return retval

# FilterMirror
#
class FilterMirror(mirrors.BasicMirrorWriter):
    def __init__(self, config=None):
        super(FilterMirror, self).__init__(config=config)
        self.config = config or {}
        self.filters = config.get('filters', [])
        self.json_entries = []

    def load_products(self, path=None, content_id=None):
        return {'content_id': content_id, 'products': {}}

    def filter_item(self, data, src, target, pedigree):
        return filters.filter_item(self.filters, data, src, pedigree)

    def insert_item(self, data, src, target, pedigree, contentsource):
        # src and target are top level products:1.0
        # data is src['products'][ped[0]]['versions'][ped[1]]['items'][ped[2]]
        # contentsource is a ContentSource if 'path' exists in data or None
        data = util.products_exdata(src, pedigree)
        if 'path' in data:
            data.update({'item_url': contentsource.url})

        self.json_entries.append(data)

# CloudImages
#
class CloudImages(object):
    '''
    '''

    # __init__
    #
    def __init__(s, cloud, series=None, region=None):
        '''
        '''
        center(s.__class__.__name__ + '.__init__')
        s.cloud  = cloud
        s.series = series
        s.region = region
        cleave(s.__class__.__name__ + '.__init__')

    @property
    def images(s):
        center(s.__class__.__name__ + '.images')
        retval = []

        # Get daily streams, change for releases
        (mirror_url, path) = util.path_from_mirror_url('https://cloud-images.ubuntu.com/daily/streams/v1/index.sjson', None)
        cdebug('    mirror_url: %s' % mirror_url)
        cdebug('          path: %s' % path)

        smirror = mirrors.UrlMirrorReader(mirror_url)

        # Change the content_id to find results for other clouds or for release images
        fl = []
        fl.append('content_id=com.ubuntu.cloud:daily:%s' % s.cloud)
        if s.series is not None:
            fl.append('release=' + s.series)
        if s.region is not None:
            fl.append('region=' + s.region)
        filter_list = filters.get_filters(fl)
        cdebug('            fl: %s' % fl)

        tmirror = FilterMirror(config={'filters': filter_list})
        try:
            tmirror.sync(smirror, path)

            try:
                # Find the latest version
                for i in tmirror.json_entries:
                    # cdebug(i)
                    cdebug(i['version_name'])
                versions = [item['version_name'] for item in tmirror.json_entries]
                versions = sorted(list(set(versions)))
                cdebug(versions)
                latest = versions[-1]

                items = [i for i in tmirror.json_entries if i['version_name'] == latest]
                for item in items:
                    retval.append(item)

            except IndexError:
                pass

            # # Print a list of the regions represented in the filtered list
            # # as an example of extracting a list of unique keys from all items
            # regions = set([item['region'] for item in tmirror.json_entries])
            # regions = sorted(list(regions))
            # print('Regions: %s' % regions)

        except IOError:
            pass

        cleave(s.__class__.__name__ + '.images')
        return retval

# vi:set ts=4 sw=4 expandtab syntax=python:
