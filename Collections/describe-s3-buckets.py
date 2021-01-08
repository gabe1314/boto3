import boto3
aws_mag_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_mag_con.client(service_name="s3")
f1={"Name": "list_backup_vaults", "Values":['BackupVaultName', 'stopped']}
f2={"Name": "instance-type", "Values":['t2.micro']}
for each in ec2_con_re.instances.filter(Filters=[f1,f2]):
    print(each)
