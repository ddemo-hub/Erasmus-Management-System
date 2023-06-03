from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class FinalFormsController(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, final_forms_service):
        AuthorizeService.__init__(self, role=role)
        self.final_forms_service = final_forms_service

    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("final_forms.html", user = current_user)
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