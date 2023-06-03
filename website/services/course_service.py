from .singleton import Singleton

from website.models import User, Course
from sqlalchemy import insert
from io import BytesIO
from website import db

class CourseService(metaclass=Singleton):
    def __init__(self, user_table, course_table, bilkent_course_table, university_table):
        self.user_table = user_table
        self.course_table = course_table
        self.bilkent_course_table = bilkent_course_table
        self.university_table = university_table

    def getBilkentCourseName(self, course_id: int):
        bilkent_course_name = self.bilkent_course_table.query.filter_by(course_id=course_id).first()
        return bilkent_course_name.course_name

    def getBilkentCoursesByName(self, course_name: str):
        course_name.lower()
        return self.bilkent_course_table.query.filter_by(course_name=course_name).first()

    def getCourseCoordinator(self, course_name: str):
        course = self.getBilkentCoursesByName(course_name=course_name).first()
        return course.course_coordinator

    def insertProposedCourse(
        self,
        course_name: str,
        course_credit: int,
        web_page: str,
        is_elective: bool,
        equivalent_course_name: str,
        university: int,
        syllabus,
    ):
        eq_course = self.getBilkentCoursesByName(equivalent_course_name)
        equivalent_bilkent_course = eq_course.course_id
        equivalent_bilkent_course_coordinator = eq_course.course_coordinator

        proposed_course = self.course_table(
            course_name=course_name,
            course_credit=course_credit,
            web_page=web_page,
            is_elective=is_elective,
            university_id=university,
            equivalent_bilkent_course=equivalent_bilkent_course,
            equivalent_bilkent_course_coordinator=equivalent_bilkent_course_coordinator,
            approval_status="waiting approval",
            syllabus=syllabus.read(),
        )
        
        db.session.add(proposed_course)
        db.session.commit()

    def getUniversityName(self, university_id: int):
        university = self.university_table.query.filter_by(university_id=university_id).first()
        return university.name

    def approveCourse(self, course_id: int):
        course = self.course_table.query.filter_by(course_id=course_id).first()
        course.approval_status = "Approved"
        db.session.commit()

    def rejectCourse(self, course_id: int):
        course = self.course_table.query.filter_by(course_id=course_id).first()
        course.approval_status = "Rejected"
        db.session.commit()

    def sendSyllabus(self, course_id: int):
        course = self.course_table.query.filter_by(course_id=course_id).first()
        file = BytesIO(course.syllabus)
        return file
