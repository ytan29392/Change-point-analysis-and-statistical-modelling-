from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load results (assuming already saved as CSV)
price_data = pd.read_csv("../data/BrentOilPrices.csv")
events_data = pd.read_csv("../data/key_events.csv")
change_points = pd.read_csv("../results/change_point_summary.csv")

@app.route('/api/prices', methods=['GET'])
def get_prices():
    return price_data.to_json(orient="records")

@app.route('/api/events', methods=['GET'])
def get_events():
    return events_data.to_json(orient="records")

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    return change_points.to_json(orient="records")

if __name__ == '__main__':
    app.run(debug=True)
