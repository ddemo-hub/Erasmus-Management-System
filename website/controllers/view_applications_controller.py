from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class ViewApplicationsController(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, view_applications_service, deadline_service):
        AuthorizeService.__init__(self, role=role)
        self.view_applications_service = view_applications_service
        self.deadline_service = deadline_service
        self.deadline_list = self.deadline_service.get_all_deadlines_format_calendar()

    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("administrator_view_applications.html", user = current_user, deadline_list = self.deadline_list)
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

    def post(self):
        if AuthorizeService.is_authorized(self):
            if "logout" in request.form:
                logout_user()
                return redirect(url_for("login"))
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
