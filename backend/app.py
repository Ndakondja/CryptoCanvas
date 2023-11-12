from flask import Flask, jsonify
from flask_cors import CORS
import data_processing
from flask import url_for

app = Flask(__name__)
CORS(app)

@app.route('/available-coins', methods=['GET'])
def available_coins():
    coins = data_processing.get_coin_names()
    return jsonify({"coins": coins})


@app.route('/getCorrelationMatrix', methods=['GET'])
def getCorrelationMatrix():
    getCorrelationMatrix
    correlation_matrix = data_processing.correlationMatrix()
    matrix = correlation_matrix.values.tolist()
    # Get the cryptocurrency labels from the column names of the DataFrame
    labels = correlation_matrix.index.tolist()
    # Return both the matrix and the labels
    return jsonify({'matrix': matrix, 'labels': labels})


@app.route('/getCoinVolatilityComparisons', methods=['GET'])
def getCoinVolatilityComparisons():
    volatilityComparison = data_processing.volatility()
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
if __name__ == '__main__':
    app.run(debug=True)
