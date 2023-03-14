from app import db
import sqlalchemy as sa


class Services(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text)
    icon_url = sa.Column(sa.Text)

    def __repr__(self):
        return f'<Service {self.name}>'
