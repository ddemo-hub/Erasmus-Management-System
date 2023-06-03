import datetime
from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class ErasmusCoordinatorDeadlineUpdate(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str, deadline_service, user_service):
        AuthorizeService.__init__(self, role=role)
        self.deadline_service = deadline_service
        self.user_service = user_service
   

    def get(self):
        if AuthorizeService.is_authorized(self):
            deadlines = self.deadline_service.get_all_deadlines()
            return render_template("erasmus_coordinator_deadline.html", 
                                    user = current_user, 
                                    deadline_service = self.deadline_service,
                                    user_service = self.user_service,
                                    deadlines = deadlines)             
        else:
            logout_user() 
            return redirect(url_for("main"))
    
    def post(self):
        if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 
        if AuthorizeService.is_authorized(self):
            if "update" in request.form:
                deadline = request.form.get('deadline')
                force = request.form.get("force")
                deadline_name = request.form.get('deadline_type')
                if deadline.__len__() > 0:
                    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%dT%H:%M")
                    if (deadline < datetime.datetime.now() and force != "on"):
                        return redirect(url_for("erasmus_coordinator_update_deadline"))
                    else:
                        deadline_s = datetime.datetime.strftime(deadline, "%d/%m/%y %H.%M")
                        deadline = self.deadline_service.update_deadline(deadline_name, deadline_s)
                        return redirect(url_for("erasmus_coordinator_homepage"))
                else:
                    return redirect(url_for("erasmus_coordinator_update_deadline"))



        else:
            logout_user() 
            return redirect(url_for("main"))  # not authorized page eklenince değiştirilecek