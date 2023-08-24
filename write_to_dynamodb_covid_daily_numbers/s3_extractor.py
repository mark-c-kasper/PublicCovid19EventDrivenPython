import csv
import boto3

s3 = boto3.client('s3')


def get_s3_data_from_bucket(file_name, version, bucket_name):
    data = get_s3_data_from_bucket_core(file_name, version, bucket_name)
    if file_name == "nyt_data.csv":
        return data
    else:
        return convert_jh_bucket_data(data)


def get_s3_data_from_bucket_core(file_name, version, bucket_name):
    csv_data = s3.get_object(Bucket=bucket_name, Key=file_name, VersionId=version)
    data = csv_data['Body'].read().decode("utf-8")
    dict_reader = csv.DictReader(data.splitlines(), delimiter=',')
    return dict_reader


def convert_jh_bucket_data(jh_data):
    return_list = {}
    for jh_row in jh_data:
        if jh_row['Country/Region'] == 'US':
            key = jh_row['Date']
            value = jh_row['Recovered']
            return_list[key] = value
    return return_list
