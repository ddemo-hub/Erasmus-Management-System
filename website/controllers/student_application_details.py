from flask import render_template, request, redirect, url_for
from flask_login import login_user
from flask.views import MethodView


class StudentApplicationDetails(MethodView):
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def get(self):
        return render_template("application_details.html", boolean=True)
    
    def post(self):
        pass