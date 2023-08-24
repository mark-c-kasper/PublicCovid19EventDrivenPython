import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
# Scan daily table and get results.
table = dynamodb.Table('covid-daily-numbers')
scan_results = table.scan(AttributesToGet=["date", "cases", "deaths", "recovered"])


# Method to convert the query results to a Dictionary to reduce the look-up times.
def get_dynamodb_results():
    results = {}
    for result in scan_results['Items']:
        key = result['date']
        results[key] = result
    return results


dict_scan_results = get_dynamodb_results()


def get_items_to_process(nyt_data, jh_data):
    unified_data = combine_nyt_jh_data(nyt_data, jh_data)
    items_to_add, possible_items_to_update = get_possible_items_to_process(unified_data)
    items_to_update = get_items_to_update(possible_items_to_update)
    return items_to_add, items_to_update


def combine_nyt_jh_data(nyt_data, jh_data):
    return_list = []
    for nyt_row in nyt_data:
        date = nyt_row['date']
        nyt_row['recovered'] = 0 if date not in jh_data else jh_data[date]
        nyt_isodate = get_date_from_data(date)
        nyt_row['date'] = nyt_isodate
        return_list.append(nyt_row)
    return return_list


def get_date_from_data(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return date.isoformat()


# Compares the dates in the data and compares them to the dates in the table scan.
# If there is no match, the data needs to be added.  Otherwise, the item may need to be updated.
def get_possible_items_to_process(data):
    items_to_add = []
    possible_items_to_update = []
    for row in data:
        row_date = row['date']
        if row_date not in dict_scan_results:
            items_to_add.append(row)
        else:
            possible_items_to_update.append(row)
    return items_to_add, possible_items_to_update


# This was not a requirement, but felt it added value in the event that any information is
# retroactively updated.
def get_items_to_update(possible_items_to_update):
    items_to_update = []
    for item in possible_items_to_update:
        scan_result = dict_scan_results[item['date']]
        if item['date'] == scan_result['date'] \
                and (item['cases'] != scan_result['cases']
                     or item['deaths'] != scan_result['deaths']
                     or ('recovered' not in scan_result
                         or item['recovered'] != scan_result['recovered'])):
            items_to_update.append(item)
    return items_to_update
