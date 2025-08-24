# AI-Rekognition-PixelLearningCo
AI-Rekognition-PixelLearningCo
Project Overview

This project demonstrates a complete CI/CD pipeline using GitHub Actions and AWS.
When images are added to the repository, they are uploaded to an Amazon S3 bucket,
analyzed with Amazon Rekognition, and the results (labels, confidence scores,
timestamps, and branch info) are logged into DynamoDB.

Pull requests log results into the beta_results table.

Merges to main log into the prod_results table.

This setup provides a branch-specific testing and production pipeline.

# 1. Set Up AWS Resources

# S3:

Create a bucket (example: pixel-learning-co).

Add a folder/prefix rekognition-input/.

# Rekognition:

Rekognition is available by default once enabled in your AWS account.

No additional setup required.

# DynamoDB:

Create two tables:

beta_results → for pull requests

prod_results → for merges

Partition key: filename (String).

# 2. Configure GitHub Secrets

In your GitHub repo, go to:
Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION (e.g., us-east-1)

S3_BUCKET (e.g., pixel-learning-co)

DYNAMODB_TABLE_BETA

DYNAMODB_TABLE_PROD

# 3. Add and Analyze Images

Place .jpg, .jpeg, or .png files in the repo’s images/ folder.

Commit and push the changes.

Pull Request → CI runs analyze_image.py → logs to beta_results.

Merge to main → CI runs analyze_image.py → logs to prod_results.

# 4. GitHub Actions Workflows

This project uses two workflows in .github/workflows/.

on_pull_request.yml

Runs when a pull request targets main. Writes results to beta_results.

name: Analyze Images on Pull Request

on:
  pull_request:
    branches: [main]

jobs:
  analyze-images:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install boto3
      - name: Run analysis
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.AWS_REGION }}
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
          DYNAMODB_TABLE_BETA: ${{ secrets.DYNAMODB_TABLE_BETA }}
          GIT_BRANCH: pr
        run: python analyze_image.py

on_merge.yml

Runs when code is pushed to main. Writes results to prod_results.

name: Analyze Images on Merge to Main

on:
  push:
    branches: [main]

jobs:
  analyze-images:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install boto3
      - name: Run analysis
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.AWS_REGION }}
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
          DYNAMODB_TABLE_PROD: ${{ secrets.DYNAMODB_TABLE_PROD }}
          GIT_BRANCH: main
        run: python analyze_image.py

# 5. Verify DynamoDB Logging

In the AWS Console:

Go to DynamoDB → Tables.

Select beta_results or prod_results.

Click Explore table items.

You should see entries like:

{
  "filename": "rekognition-input/farm-animals.jpeg",
  "labels": [
    {"Name": "Animal", "Confidence": 98.38},
    {"Name": "Chicken", "Confidence": 98.38}
  ],
  "timestamp": "2025-06-01T14:55:32Z",
  "branch": "main"
}

# 6. Local Testing (Optional)

To test locally before pushing:

Ensure your images are in the images/ folder.

Run the script with environment variables set:

S3_BUCKET=pixel-learning-co AWS_REGION=us-east-1 DYNAMODB_TABLE_PROD=prod_results GIT_BRANCH=local-testing python analyze_image.py


This will upload images to S3, analyze them with Rekognition, and save results into DynamoDB.