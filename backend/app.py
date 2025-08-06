import os
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

price_data = pd.read_csv(os.path.join(DATA_DIR, "BrentOilPrices.csv"))
events_data = pd.read_csv(os.path.join(DATA_DIR, "key_events.csv"))
change_points = pd.read_csv(os.path.join(BASE_DIR, "../results/change_point_summary.csv"))

@app.route('/api/prices', methods=['GET'])
def get_prices():
    # Convert Date column to string for JSON serialization
    price_data['Date'] = price_data['Date'].astype(str)
    return jsonify(price_data.to_dict(orient="records"))

@app.route('/api/events', methods=['GET'])
def get_events():
    events_data['Date'] = events_data['Date'].astype(str)
    return jsonify(events_data.to_dict(orient="records"))

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    change_points['Change Point Date'] = change_points['Change Point Date'].astype(str)
    return jsonify(change_points.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
