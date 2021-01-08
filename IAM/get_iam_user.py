import boto3
import datetime
session=boto3.session.Session(profile_name="default")
iam_con_re=session.resource(service_name="iam")
#Get details of any iam user

'''
iam_user_ob=iam_con_re.User("Gabriel")
print(iam_user_ob.user_name,iam_user_ob.user_id,iam_user_ob.arn,iam_user_ob.create_date.strftime("%y-%m-%d"))
'''
'''
for each_user in iam_con_re.users.all():
    print(each_user.name,each_user.user_id,each_user.arn,each_user.create_date.strftime("%y-%m-%d"))
'''
for iam_user_ob in iam_con_re.users.all():
    print(iam_user_ob)
    print(iam_user_ob.name,iam_user_ob.user_id,iam_user_ob.arn,iam_user_ob.create_date.strftime("%y-%m-%d"))