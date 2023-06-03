from .singleton import Singleton

class RoleService(metaclass=Singleton):
    def __init__(self, role_table):
        self.role_table = role_table
    
    def get_role_by_id(self, bilkent_id: int):
        role = self.role_table.query.filter_by(bilkent_id=bilkent_id).all()
        return role
