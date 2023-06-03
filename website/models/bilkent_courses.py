from website import db

class BilkentCourses(db.Model):
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_credit = db.Column(db.Integer, nullable=False)
    mandatories: db.Column(db.String(50))

    course_coordinator = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))
    host_course = db.relationship("Course", backref="bilkentcourses")
    