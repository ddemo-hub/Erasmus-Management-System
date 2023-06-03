import datetime
import json
from flask import render_template, request, redirect, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.services.faq_service import FaqService
from website.services import document_strategy

from website.services import AuthorizeService
class ErasmusCoordinatorHome(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, user_service, applications_service, deadline_service, pdf_service):
        AuthorizeService.__init__(self, role=role)
        self.user_service = user_service
        self.applications_service = applications_service
        self.deadline_service = deadline_service
        self.pdf_service = pdf_service
        self.deadline_list = self.deadline_service.get_all_deadlines_format_calendar()

    def get(self):
        if AuthorizeService.is_authorized(self):
            
            # all applications by department
            applications = self.applications_service.getApplicationsByDepartment(current_user.department)

            return render_template(
                "erasmus_coordinator_home.html", 
                user = current_user, 
                user_service = self.user_service,
                applications = applications,
                deadline_list = self.deadline_list,
            )        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 
            if "update_faq" in request.form:
                return redirect(url_for("faq_form", user=current_user))
            if "application_form" in request.form:
                application_id = request.form.get("application_form")
                application = self.applications_service.getApplicationById(application_id)
                self.applications_service.adjustStrategy(document_strategy.SendApplicationFormStrategy())
                applicationPath = self.applications_service.applyStrategy(int(application_id))
                return send_file(applicationPath, as_attachment=True, download_name=str(application.student_id) + "_application_form.pdf")
            if "pre_approval" in request.form:
                application_id = request.form.get("pre_approval")
                application = self.applications_service.getApplicationById(application_id)
                if application.application_status != "preapproval approved":
                    self.applications_service.adjustStrategy(document_strategy.SendPreapprovalStrategy())
                    preapprovalPath = self.applications_service.applyStrategy(int(application_id))
                    return send_file(preapprovalPath, as_attachment=True, download_name=str(application.student_id) + "_pre_approval_form.pdf")
                else:
                    return send_file(f"..\\forms\\signed_forms\\preapproval_form_{application.student_id}.pdf", as_attachment=True, download_name=str(application.student_id) + "_pre_approval_form.pdf")
            if "learning_agreement" in request.form:
                application_id = request.form.get("learning_agreement")
                application = self.applications_service.getApplicationById(application_id)
                self.applications_service.adjustStrategy(document_strategy.SendLearningAgreementStrategy())
                laPath = self.applications_service.applyStrategy(int(application_id))
                return send_file(laPath, as_attachment=True, download_name=str(application.student_id) + "_learning_agreement_form.pdf")
            if "approve" in request.form:
                application_id = request.form.get("approve")
                application = self.applications_service.getApplicationById(id=application_id)
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.pdf_service.sign_preapproval_form(coordinator_id=current_user.bilkent_id, student_id=application.student_id)
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="ready for mobility")
                applications = self.applications_service.getApplicationsByDepartment(current_user.department)
                return render_template("erasmus_coordinator_home.html", user = current_user, applications=applications, deadline_list = self.deadline_list,)
            if "reject" in request.form:
                application_id = request.form.get("reject")
                application = self.applications_service.getApplicationById(id=application_id)
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="placed")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                applications = self.applications_service.getApplicationsByDepartment(current_user.department)
                return render_template("erasmus_coordinator_home.html", user = current_user, applications=applications, deadline_list = self.deadline_list,)
            
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))