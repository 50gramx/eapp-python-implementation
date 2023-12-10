from ethos.elint.services.cognitive.assist.knowledge.retriever_knowledge_pb2 import RankedPage, RetrieveClosestPagesReq, \
    RetrieveClosestParasRequest, RankedPara
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails

from application_context import ApplicationContext


class RetrieverKnowledgeConsumer:

    @staticmethod
    def learn_domain_for_retriever(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails) -> (bool, str):
        stub = ApplicationContext.retriever_knowledge_service_stub()
        response = stub.LearnDomainForRetriever(access_auth_details)
        return response.meta_done, response.meta_message

    @staticmethod
    def retrieve_closest_pages(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
                               message: str, retrieve_page_count: int) -> (bool, str, [RankedPage]):
        stub = ApplicationContext.retriever_knowledge_service_stub()
        response = stub.RetrieveClosestPages(RetrieveClosestPagesReq(
            access_auth_details=access_auth_details, message=message, retrieve_page_count=retrieve_page_count))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.ranked_pages

    @staticmethod
    def retrieve_closest_paras(access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails, message: str,
                               retrieve_para_count: int) -> (bool, str, [RankedPara]):
        stub = ApplicationContext.retriever_knowledge_service_stub()
        response = stub.RetrieveClosestParas(RetrieveClosestParasRequest(
            access_auth_details=access_auth_details, message=message, retrieve_para_count=retrieve_para_count))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.ranked_paras
