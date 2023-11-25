from application import db
import enum
    
class Reviews(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    product_quality = db.Column(db.Integer)
    shipping_time = db.Column(db.Integer)
    shipping_quality = db.Column(db.Integer)
    contact_quality = db.Column(db.Integer)

class Sales(db.Model):
    date = db.Column(db.DateTime, primary_key=True)
    product = db.Column(db.String(255))
    category = db.Column(db.String(255))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    revenue = db.Column(db.Integer)
