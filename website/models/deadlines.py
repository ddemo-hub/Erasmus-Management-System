from website import db

class Deadlines(db.Model):
    """ Deadlines Table. Deadlines can be set by Erasmus Coordinators """
    
    id = db.Column(db.Integer, primary_key=True)
    
    deadline_title = db.Column(db.String(50), nullable=False)
    
    """ Deadlines are stored as String variables with the format "day/month/year hour.minute" => for example: 14/12/22 23.59 """

    deadline = db.Column(db.String(20), nullable=False)
    
    