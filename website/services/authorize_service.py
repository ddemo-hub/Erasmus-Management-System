from flask_login import current_user
from website.models import Role
from abc import ABC

class AuthorizeService(ABC):
    def __init__(self, role):
        self.authorized_role = role
    
    def is_authorized(self):
        """ Example use:
        from flask_login import login_required, logout_user
        from flask import redirect, url_for
        
        from website.services import AuthorizeService
        class StudentHome(MethodView, AuthorizeService):
            decorators = [login_required]
    
            def __init__(self, role: str):
                AuthorizeService.__init__(self, role=role)
    
            def get(self):
                if AuthorizeService.is_authorized(self) == False:
                    logout_user()
                    return redirect(url_for("your_are_not_authorized_page"))

                # If the user is authorized, move on with the rest of the functionality
                ...
        """
        
        user_role = Role.query.filter_by(bilkent_id=current_user.bilkent_id).all()
        user_role = [role.role for role in user_role]
        
        if self.authorized_role in user_role:
            return True
        else:
            return False
