from dotenv import load_dotenv
import boto3
import os

# It is necessary to check whether we can access the needed AWS buckets

load_dotenv()

print("Testing S3 connection...")
print(f"Access Key ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
print(f"Region: {os.getenv('AWS_DEFAULT_REGION')}")

s3 = boto3.client('s3')

try:
    response = s3.list_buckets()
    print("\n Successfully connected to AWS!")
    print("Buckets you can access:")
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")
except Exception as e:
    print(f"\nError connecting to AWS: {e}")

try:
    response = s3.list_objects_v2(Bucket='amzn-hotel-res-bucket', MaxKeys=5)
    print(f"\n Successfully accessed 'amzn-hotel-res-bucket'!")
    if 'Contents' in response:
        print("Files in bucket:")
        for obj in response['Contents']:
            print(f"  - {obj['Key']}")
    else:
        print("Bucket is empty or has no objects")
except Exception as e:
    print(f"\n Error accessing bucket: {e}")