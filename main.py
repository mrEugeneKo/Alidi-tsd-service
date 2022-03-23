import os
from threading import Thread
import models
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config.from_object(os.environ.get('ALIDI_TSD_SERVICE_MODE', 'config.DevelopmentConfig'))

db = SQLAlchemy(app)


@app.route("/turnon")
def turnon():
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    # вставку запускаем в отдельном потоке, чтобы не задерживать ответ
    thread = Thread(target=SaveHistory, args=(1, ip, serno, mac, device_name, ver))
    thread.start()
    return {'UTC': dt.now(), 'next_update_min': 180}


@app.route("/update")
def update():
    ip = request.args.get('ip', default='x', type=str)
    serno = request.args.get('serno', default='x', type=str)
    mac = request.args.get('mac', default='x', type=str)
    device_name = request.args.get('device_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    # вставку запускаем в отдельном потоке, чтобы не задерживать ответ
    thread = Thread(target=SaveHistory, args=(2, ip, serno, mac, device_name, ver))
    thread.start()
    return {'UTC': dt.now(), 'next_update_min': 180}


@app.route("/login")
def login():
    username = request.args.get('username', default='x', type=str)
    ip = request.remote_addr
    server_name = request.args.get('server_name', default='x', type=str)
    ver = request.args.get('ver', default='x', type=str)
    # вставку запускаем в отдельном потоке, чтобы не задерживать ответ
    thread = Thread(target=SaveLogin, args=(3, ip, username, server_name, ver))
    thread.start()
    return {'UTC': dt.now()}


def SaveHistory(operation_code, ip, serno, mac, device_name, ver):
    if ver != 'x':
        history_rec = models.HistoryRecord(
            operation_code
            , ip
            , 0
            , ver
            , ''
            , ''
        )
        device = db.session.query(models.Device).filter_by(mac=mac).first()
        db.session.remove()
        if device:
            history_rec.device_code = device.code
        else:
            devicetype = db.session.query(models.DeviceType).filter_by(description=device_name).first()
            db.session.remove()
            newdevice = models.Device(
                mac,
                serno,
                0,
                1
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


def SaveLogin(operation_code, ip, username, server_name, ver):
    if ver != 'x':
        history_rec = models.HistoryRecord(
            operation_code
            , ip
            , 0
            , ver
            , username
            , server_name
        )
        lasthistory = db.session.query(models.HistoryRecord)\
            .filter_by(ip=ip) \
            .order_by(models.HistoryRecord.created_date.desc()) \
            .first()
        db.session.remove()
        if lasthistory:
            history_rec.device_code = lasthistory.device_code
        db.session.add(history_rec)
        db.session.commit()
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if app.config.get('DEBUG'):
        # в режиме отладки работаем только по https
        app.run(host='0.0.0.0', port=8080)
    else:
        if os.environ.get('ALIDI_TSD_PROTOCOL', 'http') == 'http':
            # если в настройках http - работаем по http
            from waitress import serve
            serve(app, host='0.0.0.0', port=8080)
        else:
            # если в настройках https - работаем по https
            context = ('alidi/alidi_ru_2022_05_12.crt', 'alidi/alidi_ru_2022_05_12.txt')
            app.run(host='0.0.0.0', port=8080, ssl_context=context)
