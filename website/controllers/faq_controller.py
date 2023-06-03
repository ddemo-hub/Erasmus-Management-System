from flask import render_template, request, redirect, url_for

from flask.views import MethodView


class FAQ(MethodView):
    def __init__(self, faq_service):
        self.faq_service = faq_service

    def get(self):
        return render_template("faq_page.html", boolean=True,  all_faq = self.faq_service.getAllQuestions())
    
    
