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
