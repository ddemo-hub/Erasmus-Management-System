from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from openpyxl import Workbook
from website.services import AuthorizeService

class ErasmusCoordinatorUniversities(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, university_service, user_service, applications_service):
        AuthorizeService.__init__(self, role)
        self.university_service = university_service
        self.user_service = user_service
        self.applications_service = applications_service
    
    def get(self):
        if AuthorizeService.is_authorized(self):
            universities = self.university_service.getUniversitiesByDepartment(current_user.department)
            departments = self.university_service.getDepartments(current_user.department)
            university_dictionary = dict(zip(universities, departments))
            return render_template("erasmus_coordinator_universities.html", user = current_user, university_dictionary = university_dictionary)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))

    def post(self):
        if AuthorizeService.is_authorized(self):
            if "add_university" in request.form:
                name = request.form.get('name')
                country = request.form.get('country')
                semester = request.form.get('semester')
                department = current_user.department
                language = request.form.get('language')
                quota = int(request.form.get('quota'))
                if semester == "default":
                    flash("You haven't selected available semesters", category='error')
                elif quota <= 0:
                    flash("Quota can't be less than 1", category='error')
                else:
                    university = self.university_service.getUniversityByName(name=name)
                    if (university != None):
                        self.university_service.addDepartment(
                            department = department,
                            quota = quota,
                            university_id = university.university_id
                        )
                    else:
                        semester = semester.capitalize()
                        self.university_service.addUniversity(
                            name = name,
                            country = country,
                            semester = semester,
                            department = department,
                            language = language,
                            quota = quota
                        )
                    flash(name + " is successfully added to the system", category='success')
                return redirect(url_for("erasmus_coordinator_universities"))
            if 'update' in request.form:
                university_id = request.form.get('update')
                university = self.university_service.getUniversityById(university_id)
                department = self.university_service.getDepartment(department=current_user.department, university_id=university_id)
                name = request.form.get('update_name')
                country = request.form.get('update_country')
                semester = request.form.get('update_semester')
                language = request.form.get('update_language')
                new_quota = int(request.form.get('update_total_quota'))
                remaining_quota = int(request.form.get('update_remaining_quota'))
                old_quota = int(department.total_quota)
                new_remaining_quota = remaining_quota + new_quota - old_quota
                if new_remaining_quota < 0:
                    flash("The quota change you are attempting decreases remaining quota to a negative value", category='error')
                else:
                    semester = semester.capitalize()
                    self.university_service.updateUniversity(
                        id = university_id,
                        name = name,
                        country = country,
                        semester = semester,
                        department = current_user.department,
                        language = language,
                        total_quota = new_quota,
                        remaining_quota = new_remaining_quota
                    )
                    flash(name + " is succesfully updated", category='success')
                return redirect(url_for("erasmus_coordinator_universities"))
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))