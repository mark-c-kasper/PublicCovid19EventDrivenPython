import boto3
import datetime
import json


def publish_event(body, event_bus, event_source):
    eventbridge_client = boto3.client('events')
    detail = {
        "files": body
    }
    eventbridge_event = {
        'Detail': json.dumps(detail),
        'EventBusName': event_bus,
        'Time': datetime.datetime.now(),
        'Source': event_source,
        'DetailType': 'files_to_process'
    }
    response = eventbridge_client.put_events(Entries=[eventbridge_event])


def lambda_handler(event, context):
    if not event:
        return
    body = event['results']['body']
    event_bus = event['StatePayload']['event_bus']
    event_source = event['StatePayload']['event_source']
    if not body:
        return
    if not event_bus:
        return
    publish_event(body, event_bus, event_source)
