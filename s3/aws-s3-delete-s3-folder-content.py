import boto3
session=boto3.session.Session(profile_name="default")

bucket_name="lngm-lngm-test--jenkins-deployments"

'''

s3_re=session.resource(service_name="s3",region_name="us-east-1")
bucket_name="lngm-lngm-test--jenkins-deployments"
bucket_object=s3_re.Bucket(bucket_name)
cnt=1
for each_obj in bucket_object.objects.all():
    print(cnt,each_obj.key)
    cnt=cnt+1
'''

'''
s3_cli=session.client(service_name="s3",region_name="us-east-1")
cnt=1

for each_object in s3_cli.list_objects(Bucket=bucket_name)['Contents']:
    print(cnt,each_object['Key'])
    cnt=cnt+1

'''
'''
cnt=1
s3_cli=session.client(service_name="s3",region_name="us-east-1")
paginator = s3_cli.get_paginator('list_objects')


for each_page in paginator.paginate(Bucket=bucket_name):
    for each_object in each_page['Contents']:
        print(cnt,each_object['Key'])
        cnt=cnt+1
'''
client = session.client(service_name="s3",region_name="us-east-1")
paginator = client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket_name)

delete_us = dict(Objects=[])
for item in pages.search('Contents'):
    delete_us['Objects'].append(dict(Key=item['Key']))

    # flush once aws limit reached
    if len(delete_us['Objects']) >= 1000:
        client.delete_objects(Bucket=bucket_name, Delete=delete_us)
        delete_us = dict(Objects=[])

# flush rest
if len(delete_us['Objects']):
    client.delete_objects(Bucket=bucket_name, Delete=delete_us)