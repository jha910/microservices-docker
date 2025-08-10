from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

DB = "wfh.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS wfh
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        empNumber TEXT NOT NULL,
        empName TEXT NOT NULL,
        noOfDays INTEGER NOT NULL)''')
    conn.close()

init_db()

@app.route('/wfh', methods=['POST'])
def wfh_request():
    data = request.get_json()
    empNumber = data.get('empNumber')
    empName = data.get('empName')
    noOfDays = data.get('noOfDays')
    if not empNumber or not empName or not noOfDays:
        return jsonify(status="error", message="Fields cannot be empty"), 400
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO wfh (empNumber, empName, noOfDays) VALUES (?, ?, ?)", (empNumber, empName, noOfDays))
    conn.commit()
    conn.close()
    return jsonify(status="success", message="WFH requested successfully")

if __name__ == '__main__':
    app.run(port=5002)
