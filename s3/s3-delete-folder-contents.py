import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('lngm-lngm-test--jenkins-deployments')
bucket.objects.filter(Prefix="/Logs").delete()