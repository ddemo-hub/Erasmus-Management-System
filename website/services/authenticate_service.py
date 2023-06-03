from .singleton import Singleton

class AuthenticateService(metaclass=Singleton):
    def __init__(self, user_table, role_service):
        self.user_table = user_table
        self.role_service = role_service
    
    def authenticate(self, bilkent_id: int, password: str):
        """ Only used in the Login Page """
        user = self.user_table.query.filter_by(bilkent_id=bilkent_id).first()
        
        if (user == None) or (password != user.password):
            return False, False 
        else:
            role = self.role_service.get_role_by_id(bilkent_id)
            return user, role
