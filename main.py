import os
import models
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

@app.route("/turnon")
def turnon():
    # Use a breakpoint in the code line below to debug your script.
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)

    history_rec = models.HistoryRecord(
        1
        , ip
        , mac
        , serno
        , device_name
        , ver
    )
    db.session.add(history_rec)
    db.session.commit()
    return 'ok'  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)