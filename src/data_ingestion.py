import os
import pandas as pd
import boto3
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path
from utils.custom_exception import CustomException
from utils.general_utils import load_config
from sklearn.model_selection import train_test_split

load_dotenv()

class DataIngestion:
    def __init__(self, config):

        self.config = config["data_ingestion"]
        self.train_test_ratio = self.config["train_ratio"]

        self.bucket = self.config["bucket"]
        self.key = self.config["key"]

        self.raw_data_dir = Path(self.config["raw_data_dir"])
        self.raw_data_file = self.raw_data_dir / "Hotel_Reservations.csv"

    def download_from_s3(self) -> str:
        try:
            if os.path.exists(self.raw_data_file):
                logger.info(f"Using cached file: {self.raw_data_file}")
                return self.raw_data_file

            logger.info(f"Downloading from S3: s3://{self.bucket}/{self.key}")
            os.makedirs(os.path.dirname(self.raw_data_file), exist_ok=True)

            s3 = boto3.client("s3")
            s3.download_file(self.bucket, self.key, self.raw_data_file)

            logger.success(f"Downloaded file to {self.raw_data_file}")
            return self.raw_data_file

        except Exception as e:
            logger.error("Failed during S3 download")
            raise CustomException(e)
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(self.raw_data_file)
            train_data , test_data = train_test_split(data , test_size=1-self.train_test_ratio , random_state=42)

            train_data_file = self.raw_data_dir / "train_Hotel_Reservations.csv"
            test_data_file = self.raw_data_dir / "test_Hotel_Reservations.csv"

            train_data.to_csv(train_data_file)
            test_data.to_csv(test_data_file)

            logger.info(f"Train data saved to {train_data_file}")
            logger.info(f"Test data saved to {test_data_file}")
        
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException("Failed to split data into training and test sets ", e)
        

    def run(self) -> pd.DataFrame:
        try:
            self.download_from_s3()
            self.split_data()

            logger.info("Loading data into pandas")
            df = pd.read_csv(self.raw_data_file)

            logger.success(
                f"Loaded dataset with {len(df):,} rows and {len(df.columns)} columns"
            )
            return df

        except Exception as e:
            logger.exception("Data ingestion failed")
            raise CustomException(e)


if __name__ == "__main__":
    config = load_config('config.yaml')
    obj = DataIngestion(config)
    df = obj.run()
