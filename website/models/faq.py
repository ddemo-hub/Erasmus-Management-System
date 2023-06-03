from website import db
import datetime

class Faq(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(5), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    #date