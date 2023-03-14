from app import db


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    icon_url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    service = db.relationship("Services", backref=db.backref("devices", lazy=True))


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    device = db.relationship("Devices", backref=db.backref("conditions", lazy=True))


class Actions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    name = db.Column(db.Text, nullable=False)
    device = db.relationship("Devices", backref=db.backref("actions", lazy=True))
