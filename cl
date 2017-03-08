#!/usr/bin/env python3
#

from sys                                import stdout
from argparse                           import ArgumentParser, RawDescriptionHelpFormatter
from logging                            import basicConfig, WARNING, DEBUG
from lib.log                            import center, cleave
from lib3.cloud                         import Cloud, CloudImages

# TheApp
#
class TheApp():
    '''
    This class is just the engine that makes everything go.
    '''

    # __init__
    #
    def __init__(s, args):
        '''
        '''
        center(s.__class__.__name__ + '.__init__')
        s.args = args
        cleave(s.__class__.__name__ + '.__init__')

    def create(s):
        center(s.__class__.__name__ + '.create')

        cloud = Cloud.construct(s.args.cloud)
        retval = cloud.create(s.args.instance, s.args.series, s.args.region)
        stdout.flush()

        cleave(s.__class__.__name__ + '.create')
        return retval

    def destroy(s):
        center(s.__class__.__name__ + '.destroy')

        cloud = Cloud.construct(s.args.cloud)
        cloud.destroy(s.args.instance)

        cleave(s.__class__.__name__ + '.destroy')
        return 0

    def public_ip(s):
        center(s.__class__.__name__ + '.public_ip')

        cloud = Cloud.construct(s.args.cloud)
        print(cloud.lookup_instance_ip(s.args.instance))

        cleave(s.__class__.__name__ + '.public_ip')
        return 0

    def fqdn(s):
        center(s.__class__.__name__ + '.public_ip')

        cloud = Cloud.construct(s.args.cloud)
        print(cloud.fqdn(s.args.instance))

        cleave(s.__class__.__name__ + '.public_ip')
        return 0

    def user_and_ip(s):
        center(s.__class__.__name__ + '.public_ip')

        cloud = Cloud.construct(s.args.cloud)
        ip = cloud.lookup_instance_ip(s.args.instance)
        if cloud.ssh_user != '':
            print('%s@%s' % (cloud.ssh_user, ip))
        else:
            print(ip)

        cleave(s.__class__.__name__ + '.public_ip')
        return 0

    def list_instances(s):
        center(s.__class__.__name__ + '.list_instances')

        cloud = Cloud.construct(s.args.cloud)
        for instance in cloud.list_instances():
            print(instance)

        cleave(s.__class__.__name__ + '.list_instances')
        return 0

    def list_images(s):
        center(s.__class__.__name__ + '.list_instances')

        try:
            images = CloudImages(s.args.cloud, series=s.args.series, region=s.args.region).images
            if s.args.cloud == 'aws':
                print('%-15s  %-10s  %-10s  %-10s  %-20s  %-32s  %s' % ('Release', 'Iteam Name', 'Virt', 'Store', 'Region', 'Updated', 'AMI'))
                for image in images:
                    print('%-15s  %-10s  %-10s  %-10s  %-20s  %-32s  %s' % (image['release'], image['item_name'], image['virt'], image['root_store'], image['region'], image['updated'], image['id']))
                    if s.args.details:
                        for k, v in image.items():
                            print('    %s : %s' % (k, v))
            else:
                print('%-10s  %-10s  %-10s  %-20s  %-32s  %s' % ('Release', 'Iteam Name', 'Virt', 'Region', 'Updated', 'Image'))
                for image in images:
                    print('%-10s  %-10s  %-10s  %-20s  %-32s  %s' % (image['release'], image['item_name'], image['virt'], image['region'], image['updated'], image['id']))
                    if s.args.details:
                        for k, v in image.items():
                            print('    %s : %s' % (k, v))
        except IndexError:
            print("Unable to find any images as specified.")

        cleave(s.__class__.__name__ + '.list_instances')
        return 0

if __name__ == '__main__':
    # Command line argument setup and initial processing
    #
    app_description = '''
    '''
    app_epilog = '''
    '''

    parser = ArgumentParser(description=app_description, epilog=app_epilog, formatter_class=RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers()

    sub = subparsers.add_parser('create')
    sub.set_defaults(func=TheApp.create)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')
    sub.add_argument('instance', metavar='INSTANCE', type=str, help='')
    sub.add_argument('series', metavar='SERIES', type=str, help='')
    sub.add_argument('region', metavar='REGION', help='')

    sub = subparsers.add_parser('destroy')
    sub.set_defaults(func=TheApp.destroy)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')
    sub.add_argument('instance', metavar='INSTANCE', type=str, help='')

    sub = subparsers.add_parser('fqdn')
    sub.set_defaults(func=TheApp.fqdn)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')
    sub.add_argument('instance', metavar='INSTANCE', type=str, help='')

    sub = subparsers.add_parser('public-ip')
    sub.set_defaults(func=TheApp.public_ip)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')
    sub.add_argument('instance', metavar='INSTANCE', type=str, help='')

    sub = subparsers.add_parser('user-and-ip')
    sub.set_defaults(func=TheApp.user_and_ip)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')
    sub.add_argument('instance', metavar='INSTANCE', type=str, help='')

    sub = subparsers.add_parser('list-instances')
    sub.set_defaults(func=TheApp.list_instances)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')

    sub = subparsers.add_parser('list-images')
    sub.set_defaults(func=TheApp.list_images)
    sub.add_argument('--debug', action='store_true', default=False, help='Print out a lot of messages about what is going on.')
    sub.add_argument('--series', help='')
    sub.add_argument('--region', help='')
    sub.add_argument('--details', action='store_true', default=False, help='')
    sub.add_argument('cloud',  metavar='CLOUD',  type=str, help='')

    args = parser.parse_args()

    # If logging parameters were set on the command line, handle them
    # here.
    #
    log_format = "%(levelname)s - %(message)s"
    if args.debug:
        basicConfig(level=DEBUG, format=log_format)
    else:
        basicConfig(level=WARNING, format=log_format)

    app = TheApp(args)
    exit(args.func(app))

# vi:set ts=4 sw=4 expandtab:
