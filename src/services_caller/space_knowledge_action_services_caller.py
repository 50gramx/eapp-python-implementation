from application_context import ApplicationContext
from ethos.elint.services.product.action.space_knowledge_action_pb2 import AskQuestionRequest, DomainRankedAnswers
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails


def ask_question(access_auth_details: AccountAssistantServicesAccessAuthDetails, message: str) -> (
        bool, str, [DomainRankedAnswers]):
    stub = ApplicationContext.space_knowledge_action_service_stub()
    response = stub.AskQuestion(AskQuestionRequest(access_auth_details=access_auth_details, message=message))
    return response.response_meta.meta_done, response.response_meta.meta_message, response.domains_ranked_answers
