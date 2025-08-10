from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

DB = "leaves.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS leaves
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        empNumber TEXT NOT NULL,
        empName TEXT NOT NULL,
        leaveDays INTEGER NOT NULL)''')
    conn.close()

init_db()

@app.route('/leave', methods=['OPTIONS', 'POST'])
def leave_request():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    data = request.get_json()
    empNumber = data.get('empNumber')
    empName = data.get('empName')
    leaveDays = data.get('leaveDays')
    if not empNumber or not empName or not leaveDays:
        return jsonify(status="error", message="Fields cannot be empty"), 400
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO leaves (empNumber, empName, leaveDays) VALUES (?, ?, ?)", (empNumber, empName, leaveDays))
    conn.commit()
    conn.close()
    return jsonify(status="success", message="Leave requested successfully")


if __name__ == '__main__':
    app.run(port=5001)
