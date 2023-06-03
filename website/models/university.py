from website import db

class University(db.Model):
    """ University name and id table """

    university_id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    language_requirements = db.Column(db.String(50), nullable=False)
    departments = db.relationship("UniversityDepartments", backref="university")
    courses = db.relationship("Course", backref="university")
    image_url = db.Column(db.String(500), nullable=True)
    db.relationship("Applications", backref="university")
    
    def get_id(self):
        return self.university_id
    
