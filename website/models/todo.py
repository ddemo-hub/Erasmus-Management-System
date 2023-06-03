from website import db

class Todo(db.Model):
    """ Todo Table. One to Many Relationship with the User Table """
    task_id = db.Column(db.Integer, primary_key=True)
    
    task = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    
    def get_id(self):
        return self.task_id
    