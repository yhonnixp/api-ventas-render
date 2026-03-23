from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'ventas.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/ventas', methods=['GET', 'POST', 'DELETE'])
def ventas():
    data = load_data()
    if request.method == 'GET':
        return jsonify(data), 200
    elif request.method == 'POST':
        new_sale = request.json
        data.append(new_sale)
        save_data(data)
        return jsonify(new_sale), 201
    elif request.method == 'DELETE':
        sale_id = request.args.get('id')
        if sale_id:
            data = [s for s in data if s.get('id') != sale_id]
            save_data(data)
            return jsonify({'message': 'Eliminado'}), 200
        return jsonify({'error': 'ID requerido'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
