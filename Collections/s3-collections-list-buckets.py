import boto3
aws_mag_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_mag_con.resources(service_name="s3")
print("Here is a list of all buckets")
ec2_con_re.buckets.listBuckets()
print("bucket list")