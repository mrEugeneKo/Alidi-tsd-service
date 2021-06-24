from datetime import datetime as dt
from main import db


class HistoryRecord(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    operation_code = db.Column(db.Integer)
    ip = db.Column(db.String(16))
    mac = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    device_code = db.Column(db.Integer)
    version = db.Column(db.String(50))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    def __init__(self, operation_code, ip, mac, serial_number, device_code, version):
        self.operation_code = operation_code
        self.ip = ip
        self.mac = mac
        self.serial_number = serial_number
        self.device_code = device_code
        self.version = version
        self.time = dt.now().time()
        self.date = dt.now().date()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'operation_code': self.operation_code,
            'ip': self.ip,
            'mac': self.mac,
            'serial_number': self.serial_number,
            'device_code': self.device_code,
            'version': self.version,
            'date': self.date,
            'time': self.time
        }


class DeviceName(db.Model):
    __tablename__ = 'device'

    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<code {}>'.format(self.code)

    def serialize(self):
        return {
            'code': self.code,
            'description': self.description,
        }
