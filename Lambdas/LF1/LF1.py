import json
import boto3
import urllib3


def detect_labels(photo, bucket):
    print(photo, bucket)
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)
    result = [label['Name'] for label in response['Labels']]
    return result


def get_s3_object_custom_labels(photo, bucket):
    # Get Custom labels from request and return them as well
    client = boto3.client('s3')
    response_metadata = client.head_object(Bucket=bucket, Key=photo)['Metadata']
    if 'customlabels' in response_metadata:
        labels = response_metadata['customlabels']
        return labels.split(',')
    return []


def add_to_elastic(photo_metadata):
    http = urllib3.PoolManager()
    headers = urllib3.util.request.make_headers(basic_auth='chaitanyachawla:Hello@123')
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    url = 'https://search-photos-ko6qs6htfy7roia4kfnposm2lm.us-east-1.es.amazonaws.com/photos2/photo3/{0}'.format(
        photo_metadata['objectKey'])

    resp = http.request("POST", url, headers=headers, body=json.dumps(photo_metadata))
    print(json.loads(resp.data))


#     Do exception handling here?


def index_photo(photo, bucket, eventTime):
    labels = detect_labels(photo, bucket)
    custom_labels = get_s3_object_custom_labels(photo, bucket)
    all_labels = labels + custom_labels
    photo_metadata = {
        'objectKey': photo,
        'bucket': bucket,
        'createdTimeStamp': eventTime,
        'labels': all_labels
    }
    add_to_elastic(photo_metadata)


def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    photo = event['Records'][0]['s3']['object']['key']
    eventTime = event['Records'][0]['eventTime']
    print(bucket, photo, eventTime)
    index_photo(photo, bucket, eventTime)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


print(get_s3_object_custom_labels('Screenshot 2022-01-31 at 12.03.24 AM.png', 'photosccbd'))
