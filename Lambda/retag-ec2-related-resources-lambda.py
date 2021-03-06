import boto3
COPYABLE = ["Application", "Environment", "Function", "Name"]
def lambda_handler(event, context):
    ec2();
    elb();
    elbv2();
    return;
def ec2():
    print('Processing EC2 Instances')
    instances = boto3.resource('ec2', region_name='us-east-1').instances.all()
    for instance in instances:
        tags = [t for t in instance.tags or [] if t['Key'] in COPYABLE]
        if not tags:
            continue
        # Tag the EBS Volumes
        for vol in instance.volumes.all():
            print('Updating tags for {}'.format(vol.id))
            vol.create_tags(Tags=tags)
        # Tag the Elastic Network Interfaces
        for eni in instance.network_interfaces:
            print('Updating tags for {}'.format(eni.id))
            eni.create_tags
def elb():
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
    client = boto3.client(name, region_name='us-east-1')
    paginator = client.get_paginator('describe_load_balancers')
    for page in paginator.paginate():
        for lb in page[page_name]:
            response = client.describe_tags(**{kwname: [lb[key]]})
            lb_tags = [item for sublist in
                      [r.get('Tags', []) for r in response['TagDescriptions']]
                      for item in sublist]
            tags[lb['LoadBalancerName']] = [t for t in lb_tags if
                                            t['Key'] in COPYABLE]
            tags[lb['LoadBalancerName']].append(
                {'Key': 'Name', 'Value': lb['LoadBalancerName']})
    return tags
def _network_interfaces(filter=None):
    client = boto3.client('ec2', region_name='us-east-1')
    paginator = client.get_paginator('describe_network_interfaces')
    for page in paginator.paginate():
        for interface in page['NetworkInterfaces']:
            if filter and not filter(interface):
                continue
            yield interface
def _tag_network_interface(eni_id, tags):
    print('Updating tags for {}'.format(eni_id))
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    eni = ec2.NetworkInterface(eni_id)
    eni.create_tags(Tags=tags)