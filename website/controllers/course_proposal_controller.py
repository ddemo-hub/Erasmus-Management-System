from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from website.services import AuthorizeService
class CourseProposalController(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role, applications_service, university_service, course_service):
        AuthorizeService.__init__(self, role=role)
        self.course_service = course_service
        self.applications_service = applications_service
        self.university_service = university_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        return render_template("student_propose_course.html")

    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        if "logout" in request.form:
            logout_user() 
            return redirect(url_for("main")) 
        
        equivalent_bilkent_course = request.form["equivalent_bilkent_course"]
        is_elective = 1 if request.form["is_elective"] == "Elective" else 0
        course_credit = request.form["course_credit"]
        course_name = request.form["course_name"]
        web_page = request.form["web_page"]
        syllabus = request.files["syllabus"]

        university = self.applications_service.getMatchedUniversity(current_user.bilkent_id)

        self.course_service.insertProposedCourse(
            course_name=course_name,
            course_credit=course_credit,
            web_page=web_page,
            is_elective=is_elective,
            equivalent_course_name=equivalent_bilkent_course,
            university=university,
            syllabus=syllabus,
        )
        
        return redirect(url_for("student_preapproval"))
        
        
