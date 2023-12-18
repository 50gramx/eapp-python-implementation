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

import logging

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.entities.space_knowledge_pb2 import SpaceKnowledgeAction
from ethos.elint.services.product.action.space_knowledge_action_pb2 import DomainRankedAnswers
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    ActionAccountAssistantServiceServicer
from google.protobuf.any_pb2 import Any

from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import \
    AccessAccountAssistantConsumer
from community.gramx.fifty.zero.ethos.identity.services_caller.account_assistant_message_service_caller import \
    send_message_to_account
from community.gramx.fifty.zero.ethos.identity.services_caller.space_knowledge_action_services_caller import \
    ask_question
from support.application.tracing import trace_rpc


class ActionAccountAssistantService(ActionAccountAssistantServiceServicer):
    def __init__(self):
        super(ActionAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    async def ActOnAccountMessage(self, request, context):
        logging.info("ActionAccountAssistantService:ActOnAccountMessage")
        access_consumer = AccessAccountAssistantConsumer
        validation_done, validation_message = access_consumer.validate_account_assistant_services(
            request.access_auth_details)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            if request.space_knowledge_action == 0:
                if request.act_on_particular_domain:
                    _, _, domains_ranked_answers = ask_question(access_auth_details=request.access_auth_details,
                                                                message=request.message, ask_particular_domain=True,
                                                                space_knowledge_domain=request.space_knowledge_domain)
                else:
                    _, _, domains_ranked_answers = ask_question(access_auth_details=request.access_auth_details,
                                                                message=request.message, ask_particular_domain=False,
                                                                space_knowledge_domain=SpaceKnowledgeDomain())
                for domain_ranked_answer in domains_ranked_answers:
                    print(
                        f"{'-' * 20}{domain_ranked_answer.space_knowledge_domain.space_knowledge_domain_name}{'-' * 20}")
                    for ranked_answer in domain_ranked_answer.ranked_answers:
                        print(f"\t>{ranked_answer.para_rank}>>>{ranked_answer.answer}")
                message_sources = []
                msg, space_id, space_type_id, domain_id, context_id = self.resolve_best_answer(domains_ranked_answers)
                for domain_ranked_answer in domains_ranked_answers:
                    message_source = Any()
                    message_source.Pack(domain_ranked_answer)
                    message_sources.append(message_source)
                logging.info(f"type(message_sources):{type(message_sources)}")
                response = send_message_to_account(
                    access_auth_details=request.access_auth_details,
                    connected_account=request.connected_account,
                    message=msg,
                    message_source_space_id=space_id,
                    message_source_space_type_id=space_type_id,
                    message_source_space_domain_id=domain_id,
                    message_source_space_domain_action=SpaceKnowledgeAction.ASK_QUESTION,
                    message_source_space_domain_action_context_id=context_id,
                    message_source=message_sources
                )
                return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
            else:
                return ResponseMeta(meta_done=False, meta_message="Invalid Action Requested.")

    @staticmethod
    def resolve_best_answer(domains_ranked_answers: [DomainRankedAnswers]) -> (str, str, str, str, str):
        """ returns params for the first best answer for the first found domain else empty tuple"""
        message = "I couldn't find any answers in any page in the space."
        message_source_space_knowledge_domain = None
        source_ranked_answer = ""
        for domain_ranked_answer in domains_ranked_answers:
            for ranked_answer in domain_ranked_answer.ranked_answers:
                message = ranked_answer.answer
                source_ranked_answer = ranked_answer
                message_source_space_knowledge_domain = domain_ranked_answer.space_knowledge_domain
                break
        if message_source_space_knowledge_domain is None:
            message_source_space_id = ""
            message_source_space_type_id = ""
            message_source_space_domain_id = ""
            message_source_space_domain_action_context_id = ""
        else:
            message_source_space_id = message_source_space_knowledge_domain.space_knowledge.space.space_id
            message_source_space_type_id = message_source_space_knowledge_domain.space_knowledge.space_knowledge_id
            message_source_space_domain_id = message_source_space_knowledge_domain.space_knowledge_domain_id
            message_source_space_domain_action_context_id = source_ranked_answer.context_id
        return (
            message, message_source_space_id, message_source_space_type_id, message_source_space_domain_id,
            message_source_space_domain_action_context_id)

# find the action
# send the request to particular action
# wait for the action response
# send account assistant message
