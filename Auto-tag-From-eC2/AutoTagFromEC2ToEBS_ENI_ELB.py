import boto3

COPYABLE = ["Application", "Environment", "Function"]


def lambda_handler(event, context):
    is_test = context.function_name == 'test'  # this value is injected by SAM local
    instances = boto3.resource('ec2').instances.all()

    copyable_tag_keys = ["Application", "Environment", "Function", ]

    for instance in instances:
        copyable_tags = [t for t in instance.tags
                         if t["Key"] in copyable_tag_keys] if instance.tags else []
        if not copyable_tags:
            continue

        # Tag the EBS Volumes
        print(f"{instance.instance_id}: {instance.tags}")
        for vol in instance.volumes.all():
            print(f"{vol.attachments[0]['Device']}: {copyable_tags}")
            if not is_test:
                vol.create_tags(Tags=copyable_tags)


        # Tag the Elastic Network Interfaces
        for eni in instance.network_interfaces:
            print(f"eth{str(eni.attachment['DeviceIndex'])}: {copyable_tags}")
            if not is_test:
                eni.create_tags(Tags=copyable_tags)
                
                continue
            
        # Tag Load Balancers    
     
                
    print('Processing ELB Instances')

    def filter(i):
        return (i.get('RequesterId') == 'amazon-elb' and
                i['Description'].startswith('ELB') and
                '/' not in i['Description'])

    tags = _get_elb_tags('elb')
    for interface in _network_interfaces(filter):
        name = interface['Description'].split(' ')[1]
        if name not in tags:
            continue
        _tag_network_interface(interface['NetworkInterfaceId'], tags[name])


def elbv2():
    print('Processing ELBv2 Instances')

    def filter(i):
        return (i.get('RequesterId') == 'amazon-elb' and
                i['Description'].startswith('ELB') and
                '/' in i['Description'])

    tags = _get_elb_tags('elbv2')
    for interface in _network_interfaces(filter):
        name = interface['Description'].split('/')[1]
        if name not in tags:
            continue
        _tag_network_interface(interface['NetworkInterfaceId'], tags[name])


def _get_elb_tags(name='elb'):
    if name == 'elb':
        page_name = 'LoadBalancerDescriptions'
        key = 'LoadBalancerName'
        kwname = 'LoadBalancerNames'
    elif name == 'elbv2':
        page_name = 'LoadBalancers'
        key = 'LoadBalancerArn'
        kwname = 'ResourceArns'
    else:
        raise ValueError('Invalid name: {}'.format(name))

    tags = {}
    client = boto3.client(name)
    paginator = client.get_paginator('describe_load_balancers')
    for page in paginator.paginate():
        for lb in page[page_name]:
            response = client.describe_tags(**{kwname: [lb[key]]})
            lb_tags = [item for sublist in
                       [r.get('Tags', []) for r in response['TagDescriptions']]
                       for item in sublist]
            tags[lb['LoadBalancerName']] = [t for t in lb_tags if
                                            t["Key"] in COPYABLE]
            tags[lb['LoadBalancerName']].append(
                {'Key': 'Name', 'Value': lb['LoadBalancerName']})
    return tags


def _network_interfaces(filter=None):
    client = boto3.client('ec2')
    paginator = client.get_paginator('describe_network_interfaces')
    for page in paginator.paginate():
        for interface in page['NetworkInterfaces']:
            if filter and not filter(interface):
                continue
            yield interface


def _tag_network_interface(eni_id, tags):
    print('Updating tags for {}'.format(eni_id))
    ec2 = boto3.resource('ec2')
    eni = ec2.NetworkInterface(eni_id)
    eni.create_tags(Tags=tags)


def main():
    ec2()
    elb()
    elbv2()


if __name__ == '__main__':
    main()