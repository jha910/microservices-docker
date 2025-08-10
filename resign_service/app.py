from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

DB = "resignation.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS resignation
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        empNumber TEXT NOT NULL,
        empName TEXT NOT NULL)''')
    conn.close()

init_db()

@app.route('/resignation', methods=['OPTIONS', 'POST'])
def resignation_request():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.get_json()
    empNumber = data.get('empNumber')
    empName = data.get('empName')
    if not empNumber or not empName:
        return jsonify(status="error", message="Fields cannot be empty"), 400
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO resignation (empNumber, empName) VALUES (?, ?)", (empNumber, empName))
    conn.commit()
    conn.close()
    return jsonify(status="success", message="Resignation submitted")


if __name__ == '__main__':
    app.run(port=5003)
