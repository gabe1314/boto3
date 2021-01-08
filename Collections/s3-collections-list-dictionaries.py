import boto3
aws_mag_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_mag_con.client(service_name="s3")
print(dir(ec2_con_re))