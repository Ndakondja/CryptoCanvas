from flask import Flask, jsonify, request  # Add 'request' to the imports
from flask_cors import CORS
import data_processing
from flask import url_for
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/available-coins', methods=['GET'])
def available_coins():
    coins = data_processing.get_coin_names()
    return jsonify({"coins": coins})


@app.route('/getCorrelationMatrix', methods=['GET'])
def getCorrelationMatrix():
    time_range = request.args.get('timeRange')
    coins = request.args.get('coins', '').split(',')

    # Compute start and end dates based on the time range
    start_date, end_date = data_processing.calculate_start_date(time_range)
    
    # Call the function to compute the correlation matrix
    try:
        correlation_matrix = data_processing.compute_bitcoin_correlation(coins, start_date, end_date)
        matrix = correlation_matrix.values.tolist()
        labels = correlation_matrix.columns.tolist()
        return jsonify({'matrix': matrix, 'labels': labels})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/getCoinVolatilityComparisons', methods=['GET'])
def getCoinVolatilityComparisons():
    # Get parameters from the query string
    time_range = request.args.get('timeRange')
    coins = request.args.get('coins', '').split(',')

    # Convert date strings to datetime objects
    start_date, end_date = data_processing.calculate_start_date(time_range)
    
    volatilityComparison = data_processing.volatility(coins, start_date, end_date)
    volatility_data = volatilityComparison.reset_index().melt(id_vars=['Date'], var_name='Coin', value_name='Volatility').to_dict(orient='records')

    # Return the data in JSON format
    return jsonify(volatility_data)
   #sonify what is being returned


@app.route('/generate', methods=['GET'])
def generate():
    data_processing.generate_heatmap()

@app.route('/heatmap', methods=['POST'])
def get_heatmap():
   # data = request.json
    #selected_coins = data.get('coins', [])
    #start_date = data.get('startDate')
    #end_date = data.get('endDate')

    # ... code to generate the heatmap ...
    generate()
    # Assuming heatmap is saved as heatmap.png in the current directory
    return jsonify({"url": url_for('get_heatmap', filename='heatmap.png', _external=True)})


@app.route('/getAllCoinData', methods=['GET'])
def get_all_coin_data():
    time_range = request.args.get('timeRange', '6m')
    selected_coins = request.args.get('coins', '').split(',')

    start_date, end_date = data_processing.calculate_start_date(time_range)

    try:
        combined_coin_data = data_processing.load_selected_coins_data(selected_coins, start_date, end_date)
        return combined_coin_data.to_json(orient='table')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getMarketCapData', methods=['GET'])
def get_market_cap_data():
    time_range = request.args.get('timeRange', '6m')
    selected_coins = request.args.get('coins', '').split(',') if request.args.get('coins') else HARDCODED_COINS
    start_date, end_date = data_processing.calculate_start_date(time_range)

    try:
        market_cap_data = data_processing.calculate_avg_market_cap(selected_coins, start_date, end_date)
        return jsonify(market_cap_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getCoinStats', methods=['GET'])
def get_coin_stats():
    # Get parameters from the query string
    time_range = request.args.get('timeRange', '6m')
    selected_coins = request.args.get('coins', '').split(',')

    # Convert date strings to datetime objects
    start_date, end_date = data_processing.calculate_start_date(time_range)

    # Call the function to calculate stats
    try:
        stats = data_processing.calculate_coin_stats(selected_coins, start_date, end_date)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)