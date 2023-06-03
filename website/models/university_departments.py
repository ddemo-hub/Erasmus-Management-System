from website import db

class UniversityDepartments(db.Model):
    """ University Departments. One to Many Relationship with University """

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(10), nullable=False)
    total_quota =  db.Column(db.Integer, nullable=False)
    remaining_quota =  db.Column(db.Integer, nullable=False)
    
    university_id = db.Column(db.Integer, db.ForeignKey("university.university_id"), nullable=False)