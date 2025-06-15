import boto3
import os

# AWS Config
bucket_name = 'pixel-learning-co'
region = 'us-east-1'

# Local file path (update with your actual username)
local_image = '/Users/tracy/Desktop/pixel learning company/images/farm animals.jpeg'

# Normalize the filename for S3 (replace spaces with dashes)
filename = os.path.basename(local_image).replace(' ', '-')
s3_key = f"rekognition-input/{filename}"

# Initialize AWS clients
s3 = boto3.client('s3', region_name=region)
rekognition = boto3.client('rekognition', region_name=region)

# Upload to S3
s3.upload_file(local_image, bucket_name, s3_key)
print(f"✅ Uploaded to s3://{bucket_name}/{s3_key}")

# Call Rekognition
response = rekognition.detect_labels(
    Image={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}},
    MaxLabels=10,
    MinConfidence=80
)

# Print results
print("\n🔍 Detected labels:")
for label in response['Labels']:
    print(f"- {label['Name']}: {label['Confidence']:.2f}%")
