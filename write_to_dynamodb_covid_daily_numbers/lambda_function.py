import os
import s3_extractor as extractor
import db_writer
import data_analyzer_transformer as dat


BUCKET_NAME = os.environ['BUCKET_NAME']


def validate_event(event_files):
    if not len(event_files['files']) == 2:
        raise Exception
    if not event_files['files'][0]['file_name'] == "nyt_data.csv":
        raise Exception


def get_s3_data(event_files, event_seq):
    nyt_file_name = event_files['files'][event_seq]['file_name']
    version = event_files['files'][event_seq]['version']
    return extractor.get_s3_data_from_bucket(nyt_file_name, version, BUCKET_NAME)


def write_results(items_to_add, items_to_update):
    db_writer.add_items(items_to_add)
    db_writer.update_items(items_to_update)


def lambda_handler(event, context):
    event_files = event['detail']
    validate_event(event_files)
    nyt_data = get_s3_data(event_files, 0)
    jh_data = get_s3_data(event_files, 1)
    items_to_add, items_to_update = dat.get_items_to_process(nyt_data, jh_data)
    write_results(items_to_add, items_to_update)
    return {
        "source": event['source'],
        "job_name": "covid_daily_processing"
    }
