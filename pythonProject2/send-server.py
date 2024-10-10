import os
import time
from flask import Flask, jsonify, render_template

app = Flask(__name__)

def read_last_line(csv_filename):
    try:
        with open(csv_filename, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1]
    except FileNotFoundError:
        pass

    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    csv_filename = 'output.csv'
    last_line = read_last_line(csv_filename)
    power = 0.0

    if last_line:
        parts = last_line.strip().split(',')
        try:
            power = float(parts[262])
        except (IndexError, ValueError):
            pass

    return jsonify({'power': power})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
