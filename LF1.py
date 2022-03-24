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
    response = client.head_object(Bucket=bucket, Key=photo)
    print(response)
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
    # labels = detect_labels(photo, bucket)
    custom_labels = get_s3_object_custom_labels(photo, bucket)
    # all_labels=labels+custom_labels
    # photo_metadata = {
    #     'objectKey': photo,
    #     'bucket': bucket,
    #     'createdTimeStamp': eventTime,
    #     'labels': all_labels
    # }
    # add_to_elastic(photo_metadata)


def main():
    photo = 'chawla3.jpg'
    bucket = 'photosccbd'
    index_photo(photo, bucket, '2022-03-22T00:49:51.251Z')


if __name__ == "__main__":
    main()
