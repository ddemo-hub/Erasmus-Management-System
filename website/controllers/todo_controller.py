from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class TodoController(MethodView, AuthorizeService):
    def __init__(self, role: str, todo_service):
        AuthorizeService.__init__(self, role=role)
        self.todo_service = todo_service
   
    @login_required
    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("todo_page.html", user = current_user)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))  


    @login_required
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "add_task" in request.form:
                newtask = request.form.get('todo_input')
                self.todo_service.postTask(bilkent_id = current_user.bilkent_id, task = newtask)
                return redirect(url_for("todo_page", user = current_user))   
            if "home" in request.form:
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "todo" in request.form:
                return redirect(url_for("todo_page", user = current_user))
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("login"))
            if "delete" in request.form:   
                task_id = request.form.get('delete')
                self.todo_service.deleteTask(task_id)
                return redirect(url_for("todo_page", user = current_user))
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page")) 
    