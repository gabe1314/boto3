import boto3
aws_mag_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_mag_con.client(service_name="backup", region_name="us-east-1")
print(dir(ec2_con_re))
