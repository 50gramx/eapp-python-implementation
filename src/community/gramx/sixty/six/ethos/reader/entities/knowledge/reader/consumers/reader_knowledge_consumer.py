from ethos.elint.entities.space_knowledge_domain_file_page_para_pb2 import SpaceKnowledgeDomainFilePagePara
from ethos.elint.entities.space_knowledge_domain_file_page_pb2 import SpaceKnowledgeDomainFilePage
from ethos.elint.services.cognitive.assist.knowledge.reader_knowledge_pb2 import PageAnswer, ReadPageQuestionRequest, \
    ParaAnswer, ReadParaQuestionRequest
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails

from application_context import ApplicationContext


class ReaderKnowledgeConsumer:

    @staticmethod
    def read_page_question(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                           page: SpaceKnowledgeDomainFilePage, question: str) -> (bool, str, PageAnswer):
        stub = ApplicationContext.reader_knowledge_service_stub()
        response = stub.ReadPageQuestion(
            ReadPageQuestionRequest(access_auth_details=access_auth_details, page=page, question=question))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.page_answer

    @staticmethod
    def read_para_question(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                           para: SpaceKnowledgeDomainFilePagePara, question: str) -> (bool, str, ParaAnswer):
        stub = ApplicationContext.reader_knowledge_service_stub()
        response = stub.ReadParaQuestion(
            ReadParaQuestionRequest(access_auth_details=access_auth_details, para=para, question=question))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.para_answer
