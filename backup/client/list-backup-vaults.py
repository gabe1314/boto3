import boto3
aws_mag_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_mag_con.client(service_name="backup", region_name="us-east-1")
for each in ec2_con_re.list_backup_vaults();
    print(each)