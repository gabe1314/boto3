import boto3


def lambda_handler(event, context):
    is_test = context.function_name == 'test'  # this value is injected by SAM local
    instances = boto3.resource('ec2').instances.all()

    copyable_tag_keys = ["Application", "Function", "Environment", "Name", "System Owner"]

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