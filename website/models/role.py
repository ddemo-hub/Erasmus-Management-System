from website import db

class Role(db.Model):
    """ Role Table for Authorization. One to Many Relationship with the User Table """

    role_id = db.Column(db.Integer, primary_key=True)
    
    role = db.Column(db.String(50), nullable=False)
    
    bilkent_id = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    
    def get_id(self):
        return self.role_id
     