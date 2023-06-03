from website import db

class Course(db.Model):
    """ Course Table for Authorization. One to Many Relationship with the University Table """
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_credit = db.Column(db.Integer, nullable=False)
    syllabus = db.Column(db.LargeBinary)
    web_page = db.Column(db.String(50))
    approval_status = db.Column(db.String(50), nullable=False)
    is_elective = db.Column(db.Boolean, default=False, nullable=False)
    
    university_id = db.Column(db.Integer, db.ForeignKey("university.university_id"))
    equivalent_bilkent_course = db.Column(db.Integer, db.ForeignKey("bilkent_courses.course_id"))
    equivalent_bilkent_course_coordinator = db.Column(db.Integer, db.ForeignKey("user.bilkent_id"))

    def get_id(self):
        return self.course_id