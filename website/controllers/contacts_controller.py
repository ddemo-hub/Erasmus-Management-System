from flask import render_template, request, redirect, url_for

from flask.views import MethodView


class Contacts(MethodView):
    def __init__(self, contacts_service):
        self.contacts_service = contacts_service

    def get(self):
        return render_template("contacts_page.html", boolean=True, eclist = self.contacts_service.getAllErasmusCoordinators())
    
    
