import json

import boto3
import uuid

import urllib3


def get_keywords(search_query):
    # Query Lex to get the keywords
    client = boto3.client('lexv2-runtime')
    if search_query is None:
        return []
    response = client.recognize_text(botId='DGLZPKCKGV',
                                     botAliasId='TSTALIASID',
                                     localeId='en_US',
                                     text=search_query,
                                     sessionId=str(uuid.uuid4()))
    print(response)
    keywords=parse_keywords(response)
    results=[]
    for keyword in keywords:
        if len(keyword)<=0:
            continue
        results.append(keyword)
        if keyword[-1]=='s':
            results.append(keyword[:-1])
    print(results)
    print(keywords)
    return results
    
    
def parse_keywords(response):
    keywords = []
    slots = response['sessionState']['intent']['slots']
    if 'object1' in slots and slots['object1']:
        keywords.append(slots['object1']['value']['interpretedValue'])
    if 'object2' in slots and slots['object2']:
        keywords.append(slots['object2']['value']['interpretedValue'])
    return keywords


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
    print(data)
    results = [
        {'url': 'http://s3.amazonaws.com/{0}/{1}'.format(item['_source']['bucket'],
                                                                item['_source']['objectKey']),
         'labels': item['_source']['labels']}
        for item in data]

    return results

def lambda_handler(event, context):
    # TODO implement
    queryParams=event['queryStringParameters']
    searchQuery=None
    if 'q' in queryParams:
        searchQuery=queryParams['q']
    
    results=get_search_results(searchQuery)
    
    headers={
        'Access-Control-Allow-Origin':'*'
    }
    print(results)
    return {
        'statusCode': 200,
        'body': json.dumps(results),
        'headers': headers
    }
