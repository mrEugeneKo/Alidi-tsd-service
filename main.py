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
    return {'UTC': dt.now(), 'next_update_min': 60}


@app.route("/update")
def update():
    # Use a breakpoint in the code line below to debug your script.
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    SaveHistory(2, ip, serno, mac, device_name, ver)
    return {'UTC': dt.now(), 'next_update_min': 180}


def SaveHistory(operation_code, ip, serno, mac, device_name, ver):
    history_rec = models.HistoryRecord(
        operation_code
        , ip
        , 0
        , ver
    )
    device = db.session.query(models.Device).filter_by(mac=mac).first()
    if device:
        history_rec.device_code = device.code
    else:
        devicetype = db.session.query(models.DeviceType).filter_by(description=device_name).first()
        newdevice = models.Device(
            mac,
            serno,
            0
        )
        if devicetype:
            newdevice.devicetype_code = devicetype.code
        else:
            newdevicetype = models.DeviceType(device_name)
            db.session.add(newdevicetype)
            db.session.commit()
            newdevice.devicetype_code = newdevicetype.code
        db.session.add(newdevice)
        db.session.commit()
        history_rec.device_code = newdevice.code
    db.session.add(history_rec)
    db.session.commit()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
