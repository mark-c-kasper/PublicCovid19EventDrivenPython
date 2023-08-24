# import mypy_boto3_dynamodb as ddb
import boto3


dynamodb = boto3.resource('dynamodb')
# Scan daily table and get results.
table = dynamodb.Table('covid-daily-numbers')


def add_items(items_to_add):
    if not items_to_add:
        return
    with table.batch_writer() as writer:
        for item in items_to_add:
            writer.put_item(Item=item)


def update_items(items_to_update):
    if not items_to_update:
        return
    for item in items_to_update:
        key = item['date']
        table.update_item(Key={"date": key},
                          UpdateExpression="set cases=:c, deaths=:d, recovered=:r",
                          ExpressionAttributeValues={
                              ":c": item['cases'],
                              ":d": item['deaths'],
                              ":r": item['recovered']
                          })
