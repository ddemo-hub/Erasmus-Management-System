from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask


db = SQLAlchemy()


def create_app():
    # --------------------------------------- Create app ------------------------------------------
    app = Flask(__name__, template_folder="../website/templates")
    app.config["SECRET_KEY"] = "secretkey"
    # ---------------------------------------------------------------------------------------------

    # --------------------------- Database initialization | configuration -------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../website/database.db"
    db.init_app(app)
    # ---------------------------------------------------------------------------------------------

    # -------------------- Call the Models and create the tables or the database ------------------
    from .models import (
        User,
        Role,
        University,
        UniversityDepartments,
        Course,
        Todo,
        Applications,
        Faq,
        Deadlines,
        BilkentCourses,
    )

    with app.app_context():
        db.create_all()
    # ---------------------------------------------------------------------------------------------

    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import (
        AuthenticateService,
        RoleService,
        UserService,
        TodoService,
        UniversityService,
        FaqService,
        ApplicationsService,
        DeadlineService,
        PDFService,
        CourseService,
        AdministratorService,
        ViewApplicationsService,
        FinalFormsService,
        InternationalOfficeService,
        ContactsService,
    )

    role_service = RoleService(role_table=Role)
    authenticate_service = AuthenticateService(user_table=User, role_service=role_service)
    user_service = UserService(User)
    todo_service = TodoService(User, Todo)
    course_service = CourseService(User, Course, BilkentCourses, University)
    university_service = UniversityService(University, UniversityDepartments)
    applications_service = ApplicationsService(user_table=User, application_table=Applications, university_table=University, course_table=Course)
    deadline_service = DeadlineService(deadlines_table=Deadlines)
    pdf_service = PDFService(Applications, University, Course, BilkentCourses, User)
    faq_service = FaqService(user_table=User, faq_table=Faq)
    administrator_service = AdministratorService(User)
    view_applications_service = ViewApplicationsService(User)
    final_forms_service = FinalFormsService(User)
    international_office_service = InternationalOfficeService(User,University,Applications,UniversityDepartments)
    contacts_service = ContactsService(User,Role)

    # ---------------------------------------------------------------------------------------------

    # --------------------- Call the Views and connect them with the Services ---------------------
    from .controllers import (
        Login,
        RoleSelection,
        Main,
        Contacts,
        FAQ,
        StudentHome,
        StudentApplication,
        LearningAggrementController,
        PreApprovalController,
        CourseProposalController,
        ErasmusCoordinatorHome,
        ErasmusCoordinatorCoursesController,
        ErasmusCoordinatorUniversities,
        ErasmusCoordinatorWaitingBin,
        CourseCoordinatorController,
        TodoController,
        FaqFormController,
        InternationalOffice,
        AdministratorController,
        ViewApplicationsController,
        FinalFormsController,
        ErasmusCoordinatorCourseFransferForm,
        ErasmusCoordinatorDeadlineUpdate,
    )

    app.add_url_rule(
        "/login/", view_func=Login.as_view("login", authenticate_service=authenticate_service)
    )
    app.add_url_rule(
        "/select_role/", view_func=RoleSelection.as_view("select_role", role_service=role_service)
    )
    app.add_url_rule(
        "/", view_func=Main.as_view("main", university_service=university_service)
    )
    app.add_url_rule("/faq/", view_func=FAQ.as_view("faq", faq_service=faq_service))
    app.add_url_rule(
        "/contacts/", view_func=Contacts.as_view("contacts", contacts_service = contacts_service)
    )

    app.add_url_rule(
        "/student_home/",
        view_func=StudentHome.as_view(
            "student_home",
            role="Student",
            deadline_service=deadline_service,
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_application/",
        view_func=StudentApplication.as_view(
            "student_application",
            role="Student",
            university_service=university_service,
            applications_service=applications_service,
            pdf_service=pdf_service,
        ),
    )
    app.add_url_rule(
        "/student_learning_agreement/",
        view_func=LearningAggrementController.as_view(
            "student_learning_agreement",
            role="Student",
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_preapproval/",
        view_func=PreApprovalController.as_view(
            "student_preapproval",
            role="Student",
            applications_service=applications_service,
            course_service=course_service,
            university_service=university_service,
            pdf_service=pdf_service
        ),
    )
    app.add_url_rule(
        "/propose_course/",
        view_func=CourseProposalController.as_view(
            "student_propose_course",
            role="Student",
            course_service=course_service,
            applications_service=applications_service,
            university_service=university_service
        )
    )

    app.add_url_rule(
        "/ec/home",
        view_func=ErasmusCoordinatorHome.as_view(
            "erasmus_coordinator_homepage",
            role="Erasmus Coordinator",
            user_service=user_service,
            applications_service=applications_service,
            pdf_service=pdf_service,
            deadline_service=deadline_service,
        ),
    )
    
    app.add_url_rule(
        "/ec/courses/",
        view_func=ErasmusCoordinatorCoursesController.as_view(
            "erasmus_coordinator_courses", 
            role="Erasmus Coordinator", 
            course_service=course_service,
            deadline_service = deadline_service,
        ),
    )
    app.add_url_rule(
        "/ec/universities/",
        view_func=ErasmusCoordinatorUniversities.as_view(
            "erasmus_coordinator_universities",
            role="Erasmus Coordinator",
            user_service=user_service,
            university_service=university_service,
            applications_service = applications_service,
        ),
    )
    app.add_url_rule(
        "/ec/update_deadline",
        view_func=ErasmusCoordinatorDeadlineUpdate.as_view(
            "erasmus_coordinator_update_deadline",
            role="Erasmus Coordinator",
            user_service=user_service,
            deadline_service=deadline_service,
        )
    )
    app.add_url_rule(
        "/ec/upload_ct_form",
        view_func=ErasmusCoordinatorCourseFransferForm.as_view(
            "erasmus_coordinator_course_transfer_form",
            role="Erasmus Coordinator",
            user_service=user_service,
            applications_service=applications_service,
            university_service=university_service,
            application_id=None
        )
    )    
    app.add_url_rule(
        "/ec/wb_management/department=<department>",
        view_func=ErasmusCoordinatorWaitingBin.as_view(
            "erasmus_coordinator_waiting_bin",
            role="Erasmus Coordinator",
            user_service=user_service,
            university_service=university_service,
            applications_service = applications_service,
            deadline_service = deadline_service,
        ),
    )
    app.add_url_rule(
        "/faq/update/department=<department>",
        view_func=FaqFormController.as_view(
            "faq_form",
            role="Erasmus Coordinator",
            user_service=user_service,
            faq_service=faq_service,
        ),
    )

    app.add_url_rule(
        "/cchome/",
        view_func=CourseCoordinatorController.as_view(
            "course_coordinator_homepage",
            role="Course Coordinator",
            course_service=course_service,
            deadline_service=deadline_service,
        ),
    )
    app.add_url_rule(
        "/todo/",
        view_func=TodoController.as_view(
            "todo_page", role="Course Coordinator", todo_service=todo_service
        ),
    )

    app.add_url_rule(
        "/intoff/",
        view_func=InternationalOffice.as_view(
            "international_office_homepage", role="International Office",
            international_office_service = international_office_service,
            deadline_service = deadline_service,
        ),
    )

    app.add_url_rule(
        "/administrator_homepage",
        view_func=AdministratorController.as_view(
            "administrator_homepage",
            role="Administrator",
            administrator_service=administrator_service,
        ),
    )
    app.add_url_rule(
        "/administrator_view_applications",
        view_func=ViewApplicationsController.as_view(
            "administrator_view_applications",
            role="Administrator",
            view_applications_service=view_applications_service,
        ),
    )
    app.add_url_rule(
        "/final_forms",
        view_func=FinalFormsController.as_view(
            "final_forms", role="Administrator", final_forms_service=final_forms_service
        ),
    )
    # ---------------------------------------------------------------------------------------------

    # ------------------------------------- Login Manager -----------------------------------------
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(bilkent_id):
        return User.query.get(int(bilkent_id))

    # ---------------------------------------------------------------------------------------------

    return app
