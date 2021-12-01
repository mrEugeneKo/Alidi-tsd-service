from datetime import datetime as dt
from main import db

class BaseDB(db.Model):
    __abstract__ = True

    code = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
    def __init__(self):
        self.created_time = dt.now().time()
        self.created_date = dt.now().date()

    def __repr__(self):
        return '<code {}>'.format(self.code)


class Device(BaseDB):
    __tablename__ = 'device'

    mac = db.Column(db.String(20))
    serial_number = db.Column(db.String(20))
    devicetype_code = db.Column(db.Integer)
    invent_id = db.Column(db.String(10))
    devicemode_code = db.Column(db.Integer)

    def __init__(self, mac, serial_number, devicetype_code, devicemode_code):
        super().__init__()
        self.mac = mac
        self.serial_number = serial_number
        self.devicetype_code = devicetype_code
        self.invent_id = ''
        self.devicemode_code = devicemode_code


class HistoryRecord(BaseDB):
    __tablename__ = 'history'

    operation_code = db.Column(db.Integer)
    device_code = db.Column(db.Integer)
    ip = db.Column(db.String(16))
    version = db.Column(db.String(5))


    def __init__(self, operation_code, ip, device_code, version):
        super().__init__()
        self.operation_code = operation_code
        self.ip = ip
        self.device_code = device_code
        self.version = version


class DeviceType(BaseDB):
    __tablename__ = 'devicetype'

    description = db.Column(db.String(50))

    def __init__(self, description):
        super().__init__()
        self.description = description

class DeviceMode(BaseDB):
    __tablename__ = 'devicemode'

    description = db.Column(db.String(20))

    def __init__(self, description):
        super().__init__()
        self.description = description