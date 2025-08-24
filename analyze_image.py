import boto3
import os
import json
from datetime import datetime
from decimal import Decimal

# Get AWS config from environment variables
bucket_name = os.environ['S3_BUCKET']
region = os.environ['AWS_REGION']
table_name = os.environ['DYNAMODB_TABLE_PROD']  # Use DYNAMODB_TABLE_BETA if it's a PR

# Initialize AWS clients
s3 = boto3.client('s3', region_name=region)
rekognition = boto3.client('rekognition', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
<<<<<<< Updated upstream
table = dynamodb.Table('prod_results')

# Image paths
=======
table = dynamodb.Table(table_name)

# Image folder relative to GitHub repo
images_dir = 'images'
>>>>>>> Stashed changes
image_paths = [
    os.path.join(images_dir, f)
    for f in os.listdir(images_dir)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

# Process each image
for image_file in image_files:
    local_image_path = os.path.join(images_dir, image_file)
    filename = image_file.replace(' ', '-')
    s3_key = f"rekognition-input/{filename}"

    # Upload to S3
    s3.upload_file(local_image_path, bucket_name, s3_key)
    print(f"Uploaded to s3://{bucket_name}/{s3_key}")

    # Detect labels
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
        MaxLabels=10,
        MinConfidence=80
    )

    # Format labels
    labels = [
        {'Name': label['Name'], 'Confidence': Decimal(str(round(label['Confidence'], 2)))}
        for label in response['Labels']
    ]

    # Prepare item
    item = {
        'filename': s3_key,
        'labels': labels,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'branch': os.environ.get('GIT_BRANCH', 'local-testing')
    }

    # Save to DynamoDB
    table.put_item(Item=item)
    print(f"Saved results to DynamoDB for {filename}")
    print(json.dumps(item, indent=2, default=str))
