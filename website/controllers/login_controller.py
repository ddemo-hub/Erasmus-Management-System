from flask import render_template, request, redirect, url_for
from flask_login import login_user
from flask.views import MethodView

class Login(MethodView):
    def __init__(self, authenticate_service):
        self.authenticate_service = authenticate_service

    def get(self):
        return render_template("login_page.html")
    
    def post(self):
        try:
            bilkent_id = int(request.form.get("bilkent_id"))
            password = str(request.form.get("password"))
            
            user, role = self.authenticate_service.authenticate(bilkent_id=bilkent_id, password=password)
            
            if role == False:
                return redirect(url_for("login"))
            
            login_user(user, remember=False)
            if len(role) > 1:
                return redirect(url_for("select_role"))
            elif role[0].role == "Student":
                return redirect(url_for("student_home"))
            elif role[0].role == "Erasmus Coordinator":
                return redirect(url_for("erasmus_coordinator_homepage"))
            elif role[0].role == "Course Coordinator":  
                return redirect(url_for("course_coordinator_homepage"))
            elif role[0].role == "International Office":
                return redirect(url_for("international_office_homepage"))
            elif role[0].role == "Administrator":
                return redirect(url_for("administrator_homepage"))
            
        except:
            # In case the the credentials are incorrect
            
            # Flash Messages needs to be added here
            return render_template("login_page.html", boolean=True)

