def ec2():
    print('Processing EC2 Instances')

    instances = boto3.resource('ec2').instances.all()
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
            eni.create_tags(Tags=tags)


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
