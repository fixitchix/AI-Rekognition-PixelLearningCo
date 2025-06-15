import boto3
import os
from datetime import datetime
from decimal import Decimal


# Connect to DynamoDB and reference the correct table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('beta_results')

# AWS Config
bucket_name = 'pixel-learning-co'
region = 'us-east-1'

# Local file path (update with your actual username)
local_image = '/Users/tracy/Desktop/pixel learning company/images/farm-animals-for-kids.jpeg'

# Normalize the filename for S3 (replace spaces with dashes)
filename = os.path.basename(local_image).replace(' ', '-')
s3_key = f"rekognition-input/{filename}"

# Initialize AWS clients
s3 = boto3.client('s3', region_name=region)
rekognition = boto3.client('rekognition', region_name=region)

# Upload to S3
s3.upload_file(local_image, bucket_name, s3_key)
print(f"Uploaded to s3://{bucket_name}/{s3_key}")

# Call Rekognition
response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
    MaxLabels=10,
    MinConfidence=80
)

# Print and format results
print("\n Detected labels:")
labels = [] # This will hold the structured label info
for label in response['Labels']:
    print(f"- {label['Name']}: {label['Confidence']:.2f}%")
    labels.append({
        'Name': label['Name'],
        'Confidence': Decimal(str(round(label['Confidence'], 2)))
    })



# Create timestamp in ISO format (UTC)
timestamp = datetime.utcnow().isoformat() + 'Z'

# Get branch name (use env variable or fallback)
branch = os.environ.get('GIT_BRANCH', 'local-testing')

# Prepare item to save in DynamoDB
item = {
    'filename': s3_key,
    'labels': labels,
    'timestamp': timestamp,
    'branch': branch
}

# Write to DynamoDB
table.put_item(Item=item)
print(f"\n Results saved to DynamoDB table: beta_results")