from io import BytesIO
from website.models import Applications
from abc import ABC, abstractmethod

class BaseDocumentStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def send_document(self, id):
        pass

class SendPreapprovalStrategy(BaseDocumentStrategy):
    def __init__(self):
        self.application_table = Applications
    def send_document(self, id):
        application = self.application_table.query.filter_by(application_id = id).first()
        file = BytesIO(application.pre_approval_form) 
        if file == None:
            file = f"..\\forms\\signed_forms\\preapproval_form_{application.student_id}.pdf"
        return file

class SendApplicationFormStrategy(BaseDocumentStrategy):
    def __init__(self):
        self.application_table = Applications
    def send_document(self, id):
        application = self.application_table.query.filter_by(application_id = id).first()
        file = BytesIO(application.application_form) 
        return file

class SendLearningAgreementStrategy(BaseDocumentStrategy):
    def __init__(self):
        self.application_table = Applications
    def send_document(self, id):
        application = self.application_table.query.filter_by(application_id = id).first()
        file = BytesIO(application.learning_agreement_form) 
        return file

class SendFinalTransferFormStrategy(BaseDocumentStrategy):
    def __init__(self):
        self.application_table = Applications
    def send_document(self, id):
        application = self.application_table.query.filter_by(application_id = id).first()
        file = BytesIO(application.final_transfer_form) 
        return file