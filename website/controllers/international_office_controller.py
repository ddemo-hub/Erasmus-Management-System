from flask import render_template, redirect, url_for, request, send_file
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class InternationalOffice(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str, international_office_service, deadline_service):
        AuthorizeService.__init__(self, role=role)
        self.international_office_service = international_office_service
        self.deadline_service = deadline_service

    def get(self):
        if AuthorizeService.is_authorized(self):
            departments = self.international_office_service.getDepartments()
            return render_template("international_office_homepage.html", user=current_user, departments = departments)
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

    def post(self):
        if AuthorizeService.is_authorized(self):
            if "download" in request.form:
                # if self.deadline_service.has_passed("application_deadline"):
                department = request.form.get("downloadDepartment")
                print(department)
                file = self.international_office_service.getAppliedStudents(department)
                return send_file(file, download_name=""+department+'_applications.xlsx', as_attachment=True)
            if "upload" in request.form:
                file = request.files.get('file')
                department = request.form.get("uploadDepartment")
                self.international_office_service.place(department,file)
                return redirect(url_for("international_office_homepage", user = current_user)) 
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 
