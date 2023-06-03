from website import db
from website.models import User

class ContactsService():
    def __init__(self, user_table, role_table):
        self.user_table = user_table
        self.role_table = role_table

    def getAllErasmusCoordinators(self):
        eclist = []
        users = self.user_table.query.all()
        for user in users:
            roles = self.role_table.query.filter_by(bilkent_id=user.bilkent_id).all()
            for role in roles:
                if role.role == "Erasmus Coordinator":
                    eclist.append(user)
        return eclist