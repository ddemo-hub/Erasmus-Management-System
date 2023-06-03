from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

class RoleSelection(MethodView):
    decorators = [login_required]
    
    def __init__(self, role_service):
        self.role_service = role_service
    
    def get(self):
        roles = self.role_service.get_role_by_id(current_user.bilkent_id)
        
        if len(roles) < 2:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        roles_n_homepages = {}
        for role in roles:
            if role.role == "Erasmus Coordinator":
                roles_n_homepages["Erasmus Coordinator"] = "erasmus_coordinator_homepage"
            elif role.role == "Course Coordinator":
                roles_n_homepages["Course Coordinator"] = "course_coordinator_homepage"
            elif role.role == "International Office":
                roles_n_homepages["International Office"] = "intoff_homepage"
            elif role.role == "Administrator":
                roles_n_homepages["Administrator"] = "administrator_homepage"
            
        return render_template("role_selection_page.html", roles_n_homepages=roles_n_homepages)
        