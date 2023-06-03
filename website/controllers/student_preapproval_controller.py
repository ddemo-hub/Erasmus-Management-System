from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for, send_file
from flask.views import MethodView

from website.services import AuthorizeService


class PreApprovalController(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(
        self, role: str, applications_service, course_service, university_service, pdf_service
    ):
        AuthorizeService.__init__(self, role=role)
        self.applications_service = applications_service
        self.course_service = course_service
        self.university_service = university_service
        self.pdf_service = pdf_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        try:
            if request.args["download"] == "preapproval_form":
                preapproval_form = self.pdf_service.get_preapproval_form(student_id=current_user.bilkent_id)
                return send_file(preapproval_form, as_attachment=True, download_name="preapproval_form_template.pdf")
        except:
            pass
            
        universities = self.university_service.getAllUniversities()
        courses = self.applications_service.getSelectedCourses(student_id=current_user.bilkent_id)
        return render_template("student_preapproval_page.html", user=current_user, universities=universities, courses=courses, course_service=self.course_service)
    
    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        if "logout" in request.form:
            logout_user() 
            return redirect(url_for("main")) 
        
        universities = self.university_service.getAllUniversities()

        if "Choose" in request.form:
            courses = request.form.getlist("Choose")
            self.applications_service.addCourseSelection(student_id=current_user.bilkent_id, courses=courses)
            
            courses_list = self.applications_service.getSelectedCourses(student_id=current_user.bilkent_id)
            
            self.pdf_service.create_preapproval_form(
                current_user=current_user,
                course_selections=courses_list
            )
            
            self.applications_service.changeApplicationStatus(student_id=current_user.bilkent_id, status="waiting preapproval approval")
            
            return render_template("student_preapproval_page.html", user=current_user, universities=universities, courses=courses_list, course_service=self.course_service)