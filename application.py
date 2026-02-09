import os
import sys
import joblib
import numpy as np
from utils.general_utils import load_config
from utils.custom_exception import CustomException
from flask import Flask, render_template, request
from pathlib import Path
import pandas as pd
import boto3
from src.data_processing import DataProcessor
from dotenv import load_dotenv
from loguru import logger
from utils.s3_utils import load_s3_model

load_dotenv()

app = Flask(__name__)

try:
    logger.info("Loading configuration")
    config = load_config("config.yaml")

    artifacts_dir = Path(config["data_processing"]["proc_artifacts_dir"])

    logger.info("Initializing data processor")
    processor = DataProcessor(config)

    logger.info("Loading model from S3 using load_s3_model")
    bucket_name = config["training"]["bucket_name"]
    model_key = config["training"]["model_key"]

    local_model_path = Path(config["training"]["model_output_path"])

    local_model_path = load_s3_model(bucket_name, model_key, local_model_path)

    logger.info(f"Loading model from disk at {local_model_path}")
    loaded_model = joblib.load(local_model_path)
    logger.success("Model loaded successfully")

except Exception as e:
    logger.exception("Error during application initialization")
    raise CustomException(e, sys)


@app.route("/", methods=['GET','POST'])
def index():
    try:
        if request.method=='POST':
            logger.info("Received prediction request")
            logger.debug(f"Form data: {request.form}")

            try:
                lead_time = int(request.form['lead_time'])
                no_of_special_requests = int(request.form['no_of_special_requests'])
                avg_price_per_room = float(request.form['avg_price_per_room'])
                
                arrival_month = int(request.form['arrival_month'])
                arrival_date = int(request.form['arrival_date'])
                market_segment_type = str(request.form['market_segment_type'])
                
                no_of_week_nights = int(request.form['no_of_week_nights'])
                no_of_weekend_nights = int(request.form['no_of_weekend_nights'])
                type_of_meal_plan = str(request.form['type_of_meal_plan'])
                room_type_reserved = str(request.form['room_type_reserved'])

                features = pd.DataFrame(
                    [
                        {
                            "lead_time": lead_time,
                            "no_of_special_requests": no_of_special_requests,
                            "avg_price_per_room": avg_price_per_room,
                            "arrival_month": arrival_month,
                            "arrival_date": arrival_date,
                            "market_segment_type": market_segment_type,
                            "no_of_week_nights": no_of_week_nights,
                            "no_of_weekend_nights": no_of_weekend_nights,
                            "type_of_meal_plan": type_of_meal_plan,
                            "room_type_reserved": room_type_reserved,
                        }
                    ]
                )

                logger.info("Processing input features")
                X_processed = processor.process_input(features)
                
                logger.info("Making prediction")
                prediction = loaded_model.predict(X_processed)
                logger.success(f"Prediction: {prediction[0]}")

                return render_template('index.html', prediction=prediction[0])
            except KeyError as e:
                logger.error(f"Missing form field: {e}")
                return render_template('index.html', prediction=None, error=f"Missing required field: {e}")
            except ValueError as e:
                logger.error(f"Invalid input value: {e}")
                return render_template('index.html', prediction=None, error=f"Invalid input: {e}")
            except Exception as e:
                logger.exception("Error processing prediction request")
                return render_template('index.html', prediction=None, error="An error occurred processing your request")
        
        return render_template("index.html", prediction=None)
        
    except Exception as e:
        logger.exception("Error in index route")
        raise CustomException(e, sys)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
