from datetime import datetime as dt
from main import db


class HistoryRecord(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    operation_type = db.Column(db.Integer)
    ip = db.Column(db.String(16))
    mac = db.Column(db.String())
    serial_number = db.Column(db.String())
    device_name = db.Column(db.String())
    version = db.Column(db.String())
    time = db.Column(db.DateTime)

    def __init__(self, operation_type, ip, mac, serial_number, device_name, version):
        self.operation_type = operation_type
        self.ip = ip
        self.mac = mac
        self.serial_number = serial_number
        self.device_name = device_name
        self.version = version
        self.time = dt.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'mac': self.mac,
            'serial_number': self.serial_number,
            'device_name': self.device_name,
            'version': self.version,
            'time': self.time
        }