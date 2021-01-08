import boto3
aws_con=boto3.session.Session(profile_name="default")
ec2_con_re=aws_con.resource(service_name="ec2",region_name="us-east-1")
ec2_con_cli=aws_con.client(service_name="ec2",region_name="us-east-1")

my_inst_ob=ec2_con_re.Instances("i-02ee5caa119aca74c")
print("Stopping Instance.....")
my_inst_ob.start()
