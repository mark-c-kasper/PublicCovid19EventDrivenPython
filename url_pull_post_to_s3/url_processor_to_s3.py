import boto3
import os
import urllib.request
import urllib

s3 = boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']


def pull_new_url_data(file_name_and_urls):
    for row in file_name_and_urls:
        key = row['file_name']
        data = get_url_data(row['url'])
        write_to_tmp(key, data)
        write_to_s3(key)


def get_url_data(url):
    http_response = urllib.request.urlopen(url)
    data = http_response.read().decode("utf-8")
    return data


def write_to_tmp(key, data):
    with open(f'/tmp/{key}', 'w') as handle:
        handle.write(data)


def write_to_s3(key):
    filename = f'/tmp/{key}'
    s3.upload_file(Bucket=BUCKET_NAME, Filename=filename, Key=key)
