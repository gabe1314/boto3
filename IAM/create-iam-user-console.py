import boto3
from random import choice
import sys

def get_iam_client_object():
    session=boto3.session.Session(profile_name="default")
    iam_client=session.client(service_name="iam")
    return iam_client
def get_random_password():
    len_of_password=15
    valid_chars_for_password="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?1234567890"
    return "".join(choice(valid_chars_for_password) for each_char in range(len_of_password)) 
    
def main():
    iam_client=get_iam_client_object()
    Iam_user_name="python-test-user1"
    passwrd=get_random_password()
    PolicyARN="arn:aws:iam::aws:policy/AdministratorAccess"
    try:
        iam_client.create_user(UserName=Iam_user_name)
    except Exception as e:
        if e.response['Error']['Code']=="Entity AlreadyExists":
            print "User already Exsist".format(Iam_user_name)
            sys.exit(0)
        else:
            print "Please verify the following Error and retry"
            print e
            sys.exit((0))

    iam_client.create_user(UserName=Iam_user_name)
    iam_client.create_login_profile(UserName=Iam_user_name,Password=passwrd,PasswordResetRequired=False)
    iam_client.attach_user_policy(UserName=Iam_user_name,PolicyArn=PolicyARN)
    print "IAM User Name={} and Password={}".format(Iam_user_name,passwrd)
    return None

if __name__ == "__main__":
    main()