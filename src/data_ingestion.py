import os
import pandas as pd
import boto3
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
from ..utils.custom_exception import CustomException

load_dotenv()


class DataIngestion:
    def __init__(self, bucket: str, key: str, raw_data_path: str):
        self.bucket = bucket
        self.key = key
        self.raw_data_path = raw_data_path

    def download_from_s3(self) -> str:
        try:
            if os.path.exists(self.raw_data_path):
                logger.info(f"Using cached file: {self.raw_data_path}")
                return self.raw_data_path

            logger.info(f"Downloading from S3: s3://{self.bucket}/{self.key}")
            os.makedirs(os.path.dirname(self.raw_data_path), exist_ok=True)

            s3 = boto3.client("s3")
            s3.download_file(self.bucket, self.key, self.raw_data_path)

            logger.success(f"Downloaded file to {self.raw_data_path}")
            return self.raw_data_path

        except Exception as e:
            logger.error("Failed during S3 download")
            raise CustomException(e)

    def run(self) -> pd.DataFrame:
        try:
            self.download_from_s3()

            logger.info("Loading data into pandas")
            df = pd.read_csv(self.raw_data_path)

            logger.success(
                f"Loaded dataset with {len(df):,} rows and {len(df.columns)} columns"
            )
            return df

        except Exception as e:
            logger.exception("Data ingestion failed")
            raise CustomException(e)


if __name__ == "__main__":
    raw_data_path = "data/raw/Hotel_Reservations.csv"
    key = "training_data/Hotel Reservations.csv"
    bucket = "amzn-hotel-res-bucket"

    obj = DataIngestion(bucket, key, raw_data_path)
    df = obj.run()
