import os
import boto3

sns_client = boto3.client('sns')

SNS_TOPIC = os.environ['SNS_TOPIC']


def send_sns(event):
    run_successful = event['run_successful']
    body = f'COVID Daily Processing Status: {run_successful}'
    sns_client.publish(Message=body,
                       TopicArn=SNS_TOPIC)

def lambda_handler(event, context):
    if event['source'] != "process-new-data":
        return
    send_sns(event)
