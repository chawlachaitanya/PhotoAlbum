import json

import boto3
import uuid

import urllib3


def get_keywords(search_query):
    # Query Lex to get the keywords
    # client = boto3.client('lexv2-runtime')
    # response = client.recognize_text(botId='botId',
    #                                  botAliasId='botAliasId',
    #                                  localeId='en_US',
    #                                  text=search_query,
    #                                  sessionId=str(uuid.uuid4()))
    # msgs_from_lex = response['messages']
    return ['person', 'toy']


def get_search_results(search_query):
    keywords = get_keywords(search_query)
    if len(keywords) == 0:
        return []

    http = urllib3.PoolManager()

    url = 'https://search-photos-ko6qs6htfy7roia4kfnposm2lm.us-east-1.es.amazonaws.com/photos2/_search'

    headers = urllib3.util.request.make_headers(basic_auth='chaitanyachawla:Hello@123')
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    query = {
        "size": 10,
        "query": {
            "terms": {
                "labels": keywords,
            }
        }
    }

    resp = http.request("GET", url, headers=headers, body=json.dumps(query))
    data = json.loads(resp.data)['hits']['hits']
    results = [
        {'url': 'http://s3.amazonaws.com/{0}/{1}'.format(item['_source']['bucket'],
                                                                item['_source']['objectKey']),
         'labels': item['_source']['labels']}
        for item in data]

    return results


get_search_results('person')
