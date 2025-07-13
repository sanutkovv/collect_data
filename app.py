from flask import Flask, request, render_template
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "device_data.json"

# Инициализация файла
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/report", methods=["POST"])
def report():
    data = request.get_json()
    data['timestamp'] = datetime.utcnow().isoformat()

    # Добавим IP (если нужно)
    data['ip'] = request.headers.get("X-Forwarded-For", request.remote_addr)

    with open(DATA_FILE, "r+") as f:
        db = json.load(f)
        db.append(data)
        f.seek(0)
        json.dump(db, f, indent=2)
        f.truncate()
    return {"status": "ok"}

@app.route("/dump")
def dump_data():
    with open(DATA_FILE) as f:
        data = json.load(f)
    return {"data": data}


if __name__ == "__main__":
    app.run()
