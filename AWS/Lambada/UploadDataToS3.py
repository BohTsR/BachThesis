import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'home.plant.automation.bucket'

def lambda_handler(event, context):
    try:
        # Decode the data
        data = json.loads(event['body'])
        
        # Create a unique file name based on the current timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        device_id = data.get('device_id', 'unknown')
        file_name = f"{device_id}_{timestamp}.json"
        
        # Upload the data to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data uploaded successfully')
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }
