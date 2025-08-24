import boto3
import os
import json
from datetime import datetime
from decimal import Decimal

# AWS Config
bucket_name = 'pixel-learning-co'
region = 'us-east-1'

# Initialize AWS clients
s3 = boto3.client('s3', region_name=region)
rekognition = boto3.client('rekognition', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('prod_results')

# Image paths
image_paths = [
    '/Users/tracy/Desktop/pixel learning company/images/farm-animals.jpeg',
    '/Users/tracy/Desktop/pixel learning company/images/farm-animals-for-kids.jpeg',
    '/Users/tracy/Desktop/pixel learning company/images/baby-farm-animals.jpeg'
]

# Process each image
for local_image in image_paths:
    filename = os.path.basename(local_image).replace(' ', '-')
    s3_key = f"rekognition-input/{filename}"

    # Upload to S3
    s3.upload_file(local_image, bucket_name, s3_key)
    print(f"Uploaded to s3://{bucket_name}/{s3_key}")

    # Detect labels
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
        MaxLabels=10,
        MinConfidence=80
    )

    # Collect labels
    labels = []
    for label in response['Labels']:
        labels.append({
            'Name': label['Name'],
            'Confidence': Decimal(str(round(label['Confidence'], 2)))
        })

    # Prepare DynamoDB item
    item = {
        'filename': s3_key,
        'labels': labels,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'branch': os.environ.get('GIT_BRANCH', 'local-testing')
    }

    # Write to DynamoDB
    table.put_item(Item=item)
    print(f"Saved results to DynamoDB for {filename}")

    print("\nItem to be saved to DynamoDB:")
    print(json.dumps(item, indent=2, default=str))