import os
import boto3
from datetime import datetime


dynamodb = boto3.resource('dynamodb')
RUN_STATUS_TABLE = os.environ['RUN_STATUS_TABLE']


def record_run_status(event):
    item = get_item(event)
    table = dynamodb.Table(RUN_STATUS_TABLE)
    table.put_item(Item=item)
    

def get_item(event):
    job_name, run_successful = get_file_name_and_run_status(event)
    return {
        'job_name': job_name,
        'prior_run_successful': run_successful,
        'date_of_run': datetime.now().isoformat()
    }


def get_file_name_and_run_status(event):
    job_name = event['job_name']
    run_successful = event['run_successful']
    return job_name, run_successful


def lambda_handler(event, context):
    if event['source'] == "process-new-data":
        record_run_status(event)
    return {
        "source": event['source'],
        "run_successful": event['run_successful']
        }

