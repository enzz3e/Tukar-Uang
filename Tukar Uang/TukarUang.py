from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import locale

app = Flask(__name__)
CORS(app)

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

API_KEY = "d4f5119016e27def6d9e27a3"
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    base = data.get("base")
    target = data.get("target")
    amount = data.get("amount")

    if not base or not target or amount is None or amount < 0:
        return jsonify({"error": "Invalid input"}), 400

    try:
        # Ambil nilai tukar dari API
        response = requests.get(f"{API_URL}{base}")
        exchange_data = response.json()

        if response.status_code != 200 or "conversion_rates" not in exchange_data:
            return jsonify({"error": "Failed to fetch exchange rates"}), 500

        exchange_rate = exchange_data["conversion_rates"].get(target)

        if exchange_rate is None:
            return jsonify({"error": "Invalid currency code"}), 400

        # Konversi mata uang
        converted_amount = amount * exchange_rate
        formatted_amount = locale.format_string("%.2f", converted_amount, grouping=True)

        return jsonify({
            "base": base,
            "target": target,
            "amount": amount,
            "exchange_rate": exchange_rate,
            "converted_amount": formatted_amount
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
