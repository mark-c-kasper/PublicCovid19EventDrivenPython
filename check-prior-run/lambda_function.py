import boto3
from boto3.dynamodb.conditions import Key
import os


# S3
s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
# DynamoDB
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
TABLE_KEY = os.environ['TABLE_KEY']
TABLE_ATTRIBUTE_TO_GET = os.environ['TABLE_ATTRIBUTE_TO_GET']
# EventBridge
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']


def get_prior_run_status():
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(Select="SPECIFIC_ATTRIBUTES",
                           ProjectionExpression=TABLE_ATTRIBUTE_TO_GET,
                           KeyConditionExpression=Key(TABLE_KEY).eq("covid_daily_processing"))
    return response['Items']


def get_failed_versions():
    failed_files = []
    for file_name in ['nyt_data.csv', 'jh_data.csv']:
        failed_files.append(get_failed_version(file_name))
    return failed_files
    

def get_failed_version(file_name):
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_name)
    version = response['VersionId']
    return {"file_name": file_name, "version": version}


def lambda_handler(event, context):
    run_status = get_prior_run_status()
    if not run_status:
        return {}
    elif run_status[0][TABLE_ATTRIBUTE_TO_GET] is True:
        return {}
    return {
        "event_bus": EVENT_BUS_NAME,
        "event_source": "process-prior-run",
        "body": get_failed_versions()
    }
