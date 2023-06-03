from flask import flash, render_template, request, redirect, send_file, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService, document_strategy

class ErasmusCoordinatorCourseFransferForm(MethodView):
    def __init__(self, role: str, user_service, applications_service,university_service, application_id):
        AuthorizeService.__init__(self, role=role)
        self.user_service = user_service
        self.applications_service = applications_service
        self.application_id = application_id
        self.university_service=university_service
        self.application_list = []
        for application in self.applications_service.getApplicationsByDepartment(current_user.department):
            if (application.application_status == "ready for mobility"
                    or application.application_status == "under board inspection"):
                self.application_list.append(application)
    
    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template(
                "erasmus_coordinator_course_transfer_form.html",
                user=current_user,
                user_service=self.user_service,
                applications_service=self.applications_service,
                application_list=self.application_list,
                application_id=self.application_id,
                university_service=self.university_service
            )

    
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 
            if "application_get" in request.form:
                app_id = request.form.get("application_id_radio")
                print(app_id)
                return render_template(
                    "erasmus_coordinator_course_transfer_form.html",
                    user=current_user,
                    user_service=self.user_service,
                    applications_service=self.applications_service,
                    application_list=self.application_list,
                    application_id=app_id,
                    university_service=self.university_service
                )
            if "download_preapproval" in request.form:
                app_id = request.form.get("download_preapproval")
                self.applications_service.adjustStrategy(document_strategy.SendPreapprovalStrategy())
                file = self.applications_service.applyStrategy(int(app_id))
                if file != None:
                    return send_file(file, as_attachment=True, download_name=app_id + "_preapproval.pdf")
                else:
                    return render_template(
                    "erasmus_coordinator_course_transfer_form.html",
                    user=current_user,
                    user_service=self.user_service,
                    applications_service=self.applications_service,
                    application_list=self.application_list,
                    application_id=app_id,
                    university_service=self.university_service
                )
            if "upload_ct" in request.form:
                app_id = request.form.get("upload_ct")
                ct_form = request.files['file']
                if ct_form != None and ct_form.filename != "":
                    uploaded = self.applications_service.uploadCourseTransfer(app_id, ct_form)
                    
                return render_template(
                    "erasmus_coordinator_course_transfer_form.html",
                    user=current_user,
                    user_service=self.user_service,
                    applications_service=self.applications_service,
                    application_list=self.application_list, 
                    application_id=app_id,
                    university_service=self.university_service
                )

            if "download_ct" in request.form:
                app_id = request.form.get("download_ct")
                self.applications_service.adjustStrategy(document_strategy.SendFinalTransferFormStrategy())
                file = self.applications_service.applyStrategy(int(app_id))
                return send_file(file, as_attachment=True, download_name=app_id + "_course_transfer.pdf")

            if "delete_ct" in request.form:
                app_id = request.form.get("delete_ct")
                self.applications_service.deleteCourseTransfer(app_id)

                return render_template(
                    "erasmus_coordinator_course_transfer_form.html",
                    user=current_user,
                    user_service=self.user_service,
                    applications_service=self.applications_service,
                    application_list=self.application_list,
                    application_id=app_id,
                    university_service=self.university_service
                )
            
            return render_template(
                "erasmus_coordinator_course_transfer_form.html",
                user=current_user,
                user_service=self.user_service,
                applications_service=self.applications_service,
                application_list=self.application_list,
                application_id=app_id,
                university_service=self.university_service
            )
        else:
            logout_user()
            return redirect(url_for("main"))
