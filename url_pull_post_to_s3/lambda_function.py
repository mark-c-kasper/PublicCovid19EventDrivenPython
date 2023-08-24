import os
import url_processor_to_s3 as upts
import s3_key_version_getter as skvg

EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
NYT_URL = os.environ['NYT_URL']
JH_URL = os.environ['JH_URL']

file_name_and_urls = [
    {
        "file_name": "nyt_data.csv",
        "url": NYT_URL
    },
    {
        "file_name": "jh_data.csv",
        "url": JH_URL
    }
]


def lambda_handler(event, context):
    upts.pull_new_url_data(file_name_and_urls)
    return {
        "event_bus": EVENT_BUS_NAME,
        "event_source": "process-new-data",
        "body": skvg.get_file_names_and_versions(file_name_and_urls)
    }
