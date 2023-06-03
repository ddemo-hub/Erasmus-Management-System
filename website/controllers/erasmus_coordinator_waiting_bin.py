from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from openpyxl import Workbook
from website.services import AuthorizeService


class ErasmusCoordinatorWaitingBin(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(
        self, role: str, university_service, user_service, applications_service, deadline_service
    ):
        AuthorizeService.__init__(self, role)
        self.university_service = university_service
        self.user_service = user_service
        self.applications_service = applications_service
        self.deadline_service = deadline_service
        self.deadline_list = self.deadline_service.get_all_deadlines_format_calendar()

    def get(self, department):
        if AuthorizeService.is_authorized(self):
            universities = self.university_service.getUniversitiesByDepartment(
                current_user.department
            )
            departments = self.university_service.getDepartments(current_user.department)
            university_dictionary = dict(zip(universities, departments))
            applications = self.applications_service.getApplicationsByStatus(
                status="waiting bin", dep=current_user.department
            )
            return render_template(
                "erasmus_coordinator_waiting_bin.html",
                user=current_user,
                university_dictionary=university_dictionary,
                applications=applications,
                deadline_service=self.deadline_service,
                deadline_list=self.deadline_list,
            )
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

    def post(self, department):
        if AuthorizeService.is_authorized(self):
            if "waiting_bin" in request.form:
                wb = Workbook()
                ws = wb.active
                ws.title = "Waiting Bin"
                ws.append(["Ranking", "Student ID", "Name"])
                applications = self.applications_service.getApplicationsByStatus(
                    status="waiting bin", dep=current_user.department
                )
                for application in applications:
                    student_id = application.student_id
                    student = self.user_service.getUserById(student_id)
                    ws.append([application.ranking, student_id, student.name])
                wb.save("website\static\waiting_bin.xlsx")
                return send_file(
                    "static\waiting_bin.xlsx",
                    as_attachment=True,
                    download_name=current_user.department + "_waiting_bin.xlsx",
                )
            if "place" in request.form:
                universities = self.university_service.getUniversitiesByDepartment(
                    current_user.department
                )
                departments = self.university_service.getDepartments(current_user.department)
                university_dictionary = dict(zip(universities, departments))
                application_id = request.form.get("place")
                application = self.applications_service.getApplicationById(id=application_id)
                app_period_id = application.application_period_id
                selected_university_name = request.form.get("select_university")
                university = self.university_service.getUniversityByName(selected_university_name)
                if university != None:
                    department = self.university_service.getDepartment(
                        department=current_user.department, university_id=university.university_id
                    )
                    self.university_service.updateDepartment(
                        department=current_user.department,
                        total_quota=department.total_quota,
                        remaining_quota=department.remaining_quota - 1,
                        university_id=university.university_id,
                    )
                    self.applications_service.changeApplicationStatus(
                        student_id=application.student_id, status="placed"
                    )
                    self.applications_service.matchWithUniversity(
                        student_id=application.student_id, university_id=university.university_id
                    )
                applications = self.applications_service.getApplicationsByStatus(
                    status="waiting bin", dep=current_user.department
                )
                return render_template(
                    "erasmus_coordinator_waiting_bin.html",
                    application_period_id=app_period_id,
                    user=current_user,
                    university_dictionary=university_dictionary,
                    applications=applications,
                    deadline_list=self.deadline_list,
                )
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
