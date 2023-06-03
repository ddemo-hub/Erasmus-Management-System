from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ User Table for Authentication """
    
    bilkent_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(5), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    mail = db.Column(db.String(50), nullable=True)
    role = db.relationship("Role", backref="user")
    courses = db.relationship("Course", backref="user")                 # Course Coordinator 
    todo = db.relationship("Todo", backref="user")                      # Course Coordinator  
    applications = db.relationship("Applications", backref="user")      # Student    
    bilkent_courses = db.relationship("BilkentCourses", backref="user") # Course Coordinator
    
    def get_id(self):
        return self.bilkent_id
    
