import os
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']


def get_file_names_and_versions(file_name_and_urls):
    return_list = []
    for row in file_name_and_urls:
        return_list.append(get_file_name_and_version(row['file_name']))
    return return_list


def get_file_name_and_version(key):
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    version = response['VersionId']
    return {"file_name": key, "version": version}
