from flask import render_template, request, redirect, url_for, send_file, flash
from flask_login import login_required, logout_user, current_user
from flask.views import MethodView

from website.services import AuthorizeService


class StudentApplication(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, university_service, applications_service, pdf_service):
        AuthorizeService.__init__(self, role=role)
        self.university_service = university_service
        self.applications_service = applications_service
        self.pdf_service = pdf_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        try:
            if request.args["download"] == "application_form":
                application_form_template = self.pdf_service.get_application_form(current_user.bilkent_id)
                return send_file(application_form_template, as_attachment=True, download_name="application_form_template.pdf")
        except:
            pass
        
        universities = self.university_service.getUniversitiesByDepartment(current_user.department)
        current_selections = self.applications_service.getUniversitySelections(
            current_user.bilkent_id
        )
        return render_template(
            "student_application_page.html",
            universities=universities,
            current_selections=current_selections,
        )

    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        if "logout" in request.form:
            logout_user() 
            return redirect(url_for("main")) 
        
        applicant = self.applications_service.getApplicationByStudentId(current_user.bilkent_id)
        
        universities = self.university_service.getUniversitiesByDepartment(current_user.department)
        
        if applicant.cgpa < 2.5:
            flash("Your CGPA is not high enough to apply Erasmus", "!cgpa")
            return render_template(
                "student_application_page.html",
                universities=universities,
                current_selections=[],
            )
        
        try:
            selections = []
            for university in request.form:
                if (request.form[university] != "None") and ((request.form[university] in selections) ==False):
                    selections.append(request.form[university])
                else:
                    selections.append(None)

            self.applications_service.insertUniversitySelections(current_user.bilkent_id, selections)
        except:
            pass

        current_selections = self.applications_service.getUniversitySelections(
            current_user.bilkent_id
        )
        
        if len(request.files) == 1:
            file = request.files["file"]
            self.pdf_service.upload_application_form(file=file, student_id=current_user.bilkent_id)
            self.applications_service.changeApplicationStatus(student_id=current_user.bilkent_id, status="applied")
        else:
            self.pdf_service.create_application_form(current_user, current_selections)
        
        flash("Application Successful", "success")
        return render_template(
            "student_application_page.html",
            universities=universities,
            current_selections=current_selections,
        )