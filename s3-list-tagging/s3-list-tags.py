import boto3

def lambda_handler(event, context):
    s3();
    return;
def s3 = boto3.client('s3')
    result = s3.get_bucket_tagging(Bucket='adc-to-s3-us-east-1')
    print(result)


##### Output {'ResponseMetadata': {'RequestId': '4250020B00671B5E', 'HostId': 'wHvHIL00+Ie3TqOeGw33B5ngJuJ0jbwB67NoICT7k9lZ3KUeiCDNW/uMWgfq7bYoOEPH6gCTNVI=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'wHvHIL00+Ie3TqOeGw33B5ngJuJ0jbwB67NoICT7k9lZ3KUeiCDNW/uMWgfq7bYoOEPH6gCTNVI=', 'x-amz-request-id': '4250020B00671B5E', 'date': 'Thu, 22 Oct 2020 21:28:34 GMT', 'transfer-encoding': 'chunked', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'TagSet': [{'Key': 'Bucket', 'Value': 'adc-to-s3-us-east-1'}, {'Key': 'Application', 'Value': 'Infrastructure'}]}




##### Error -- Below we need to make an expection for. 
##### result = s3.get_bucket_tagging(Bucket='sigue-inventory')
####  Traceback (most recent call last):
#####  File "<stdin>", line 1, in <module>
#####  File "/Users/gabrielsandoval/Documents/Scripts/python/s3/boto3/venv/src/botocore/botocore/client.py", line 357, in _api_call
#####    return self._make_api_call(operation_name, kwargs)
#####  File "/Users/gabrielsandoval/Documents/Scripts/python/s3/boto3/venv/src/botocore/botocore/client.py", line 676, in _make_api_call
#####    raise error_class(parsed_response, operation_name)
##### botocore.exceptions.ClientError: An error occurred (NoSuchTagSet) when calling the GetBucketTagging operation: The TagSet does not exist

######### Tags_We_Want_To_Set 'TagSet': [{'Key': 'Bucket', 'Value': '$BUCKET_NAME'}, {'Key': 'Application', 'Value': 'Infrastructure'}]}

result = s3.get_bucket_tagging().buckets.al()