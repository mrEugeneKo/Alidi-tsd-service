import os
import models
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config.from_object(os.environ.get('ALIDI_TSD_SERVICE_MODE', 'config.DevelopmentConfig'))

db = SQLAlchemy(app)


@app.route("/turnon")
def turnon():
    # Use a breakpoint in the code line below to debug your script.
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    SaveHistory(1, ip, serno, mac, device_name, ver)
    return {'UTC':  dt.now(), 'next_update_min': 120}

@app.route("/update")
def update():
    # Use a breakpoint in the code line below to debug your script.
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    SaveHistory(2, ip, serno, mac, device_name, ver)
    return {'UTC':  dt.now(), 'next_update_min': 180}

def SaveHistory(operation_code, ip, serno, mac, device_name, ver):
    history_rec = models.HistoryRecord(
        operation_code
        , ip
        , mac
        , serno
        , 0
        , ver
    )
    if device_name != 'x':
        device = db.session.query(models.DeviceName).filter_by(description=device_name).first()
        if device:
            history_rec.device_code = device.code
        else:
            device = models.DeviceName(device_name)
            db.session.add(device)
            db.session.commit()
            history_rec.device_code = device.code

    db.session.add(history_rec)
    db.session.commit()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
