import joblib
import numpy as np
from utils.general_utils import load_config
from flask import Flask, render_template, request
from pathlib import Path
import pandas as pd

from src.data_processing import DataProcessor

app = Flask(__name__)
config = load_config("config.yaml")

artifacts_dir = Path(config["data_processing"]["proc_artifacts_dir"])

processor = DataProcessor(config)
loaded_model = joblib.load(config["training"]["model_output_path"])

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=='POST':
        print(request.form)

        lead_time = int(request.form['lead_time'])
        no_of_special_requests = int(request.form['no_of_special_requests'])
        avg_price_per_room = float(request.form['avg_price_per_room'])
        
        arrival_month = int(request.form['arrival_month'])
        arrival_date = int(request.form['arrival_date'])
        market_segment_type = str(request.form['market_segment_type'])
        
        no_of_week_nights = int(request.form['no_of_week_nights'])
        no_of_weekend_nights = int(request.form['no_of_weekend_nights'])
        type_of_meal_plan =str(request.form['type_of_meal_plan'])
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

        X_processed = processor.process_input(features)
        prediction = loaded_model.predict(X_processed)

        return render_template('index.html', prediction = prediction[0])
    return render_template("index.html", prediction=None)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
