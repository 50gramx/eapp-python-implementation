from application_context import ApplicationContext
from ethos.elint.entities import space_knowledge_domain_pb2
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import \
    SpaceKnowledgeServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_inferred.access_space_knowledge_domain_inferred_pb2 import \
    SpaceKnowledgeDomainInferredServicesAccessAuthDetails, SpaceKnowledgeDomainInferredAccessTokenRequest


def space_knowledge_domain_inferred_access_token_caller(
        access_auth_details: SpaceKnowledgeServicesAccessAuthDetails,
        space_knowledge_domain_inferred: space_knowledge_domain_pb2.SpaceKnowledgeDomainInferred
) -> (bool, str, SpaceKnowledgeDomainInferredServicesAccessAuthDetails):
    request = SpaceKnowledgeDomainInferredAccessTokenRequest(
        access_auth_details=access_auth_details,
        space_knowledge_domain_inferred=space_knowledge_domain_inferred)
    stub = ApplicationContext.access_space_knowledge_domain_inferred_service_stub()
    response = stub.SpaceKnowledgeDomainInferredAccessToken(request)
    return (response.response_meta.meta_done,
            response.response_meta.meta_message,
            response.access_auth_details)


def validate_space_knowledge_domain_inferred_services_caller(
        access_auth_details: SpaceKnowledgeDomainInferredServicesAccessAuthDetails) -> (bool, str):
    stub = ApplicationContext.access_space_knowledge_domain_inferred_service_stub()
    response = stub.ValidateSpaceKnowledgeDomainInferredServices(access_auth_details)
    return response.meta_done, response.meta_message