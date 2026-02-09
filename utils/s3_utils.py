import boto3
import sys
import os
from pathlib import Path
from loguru import logger
from utils.custom_exception import CustomException


class S3Progress:
    def __init__(self):
        self._seen_so_far = 0

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        mb = self._seen_so_far / (1024 * 1024)
        logger.info(f"Downloaded {mb:.2f} MB")


def load_s3_file(bucket_name, s3_key, local_file_path):
    try:
        logger.info(f"Checking file in S3: s3://{bucket_name}/{s3_key}")

        s3 = boto3.client("s3")

        try:
            s3.head_object(Bucket=bucket_name, Key=s3_key)
            logger.info("File found in S3")
        except Exception:
            raise CustomException(
                f"File not found in S3 at key: {s3_key}", sys
            )

        local_file_path = Path(local_file_path)
        local_file_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting download to {local_file_path}")

        s3.download_file(
            bucket_name,
            s3_key,
            str(local_file_path),
            Callback=S3Progress()
        )

        logger.success(f"File downloaded successfully to {local_file_path}")

        if not local_file_path.exists() or local_file_path.stat().st_size == 0:
            raise CustomException("Downloaded file is empty or missing", sys)

        return local_file_path

    except CustomException:
        raise
    except Exception as e:
        logger.exception("Error downloading file from S3")
        raise CustomException(e, sys)
