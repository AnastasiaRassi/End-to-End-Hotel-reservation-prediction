import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class DataIngestion:
    def __init__(self, bucket, key, local_path):
        self.bucket = bucket
        self.key = key
        self.local_path = local_path

    def download_from_s3(self):
        # Download file from S3 if not already cached locally
        if os.path.exists(self.local_path):
            print(f" Using cached file: {self.local_path}")
            return self.local_path
        
        print(f"Downloading from S3: s3://{self.bucket}/{self.key}")
        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
        
        s3 = boto3.client('s3')
        s3.download_file(self.bucket, self.key, self.local_path)
        print(f"Downloaded to {self.local_path}")
        return self.local_path

    def run(self):
        # Load flight delay data from S3 (with local caching)
        self.download_from_s3()
        
        print("Loading data into pandas...")
        df = pd.read_csv(self.local_path)
        print(f"✓ Loaded {len(df):,} rows and {len(df.columns)} columns")
        
        return df

local_path = 'data/raw/Hotel_Reservations.csv'
key = 'training_data/Hotel Reservations.csv'
bucket = 'amzn-hotel-res-bucket'

obj = DataIngestion(bucket, key, local_path)
obj.run()