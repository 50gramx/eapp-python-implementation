#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.services.product.action.space_knowledge_action_pb2 import AskQuestionRequest, DomainRankedAnswers
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails

from application_context import ApplicationContext


class SpaceKnowledgeActionConsumer:

    @staticmethod
    def ask_question(access_auth_details: AccountAssistantServicesAccessAuthDetails, message: str,
                     ask_particular_domain: bool, space_knowledge_domain: SpaceKnowledgeDomain) -> (
            bool, str, [DomainRankedAnswers]):
        stub = ApplicationContext.space_knowledge_action_service_stub()
        response = stub.AskQuestion(AskQuestionRequest(access_auth_details=access_auth_details, message=message,
                                                       ask_particular_domain=ask_particular_domain,
                                                       space_knowledge_domain=space_knowledge_domain))
        return response.response_meta.meta_done, response.response_meta.meta_message, response.domains_ranked_answers
