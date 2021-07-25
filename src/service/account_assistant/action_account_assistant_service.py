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

from google.protobuf.any_pb2 import Any

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    ActionAccountAssistantServiceServicer
from services_caller.account_assistant_message_service_caller import send_message_to_account
from services_caller.account_assistant_service_caller import validate_account_assistant_services_caller
from services_caller.space_knowledge_action_services_caller import ask_question


class ActionAccountAssistantService(ActionAccountAssistantServiceServicer):
    def __init__(self):
        super(ActionAccountAssistantService, self).__init__()
        self.session_scope = self.__class__.__name__

    def ActOnAccountMessage(self, request, context):
        logging.info("ActionAccountAssistantService:ActOnAccountMessage")
        validation_done, validation_message = validate_account_assistant_services_caller(request.access_auth_details)
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
                                                                space_knowledge_domain=SpaceKnowledgeDomain)
                for domain_ranked_answer in domains_ranked_answers:
                    print(
                        f"{'-' * 20}{domain_ranked_answer.space_knowledge_domain.space_knowledge_domain_name}{'-' * 20}")
                    for ranked_answer in domain_ranked_answer.ranked_answers:
                        print(f"\t>{ranked_answer.para_rank}>>>{ranked_answer.answer}")
                message_sources = []
                for domain_ranked_answer in domains_ranked_answers:
                    message_source = Any()
                    message_source.Pack(domain_ranked_answer)
                    message_sources.append(message_source)
                response = send_message_to_account(
                    access_auth_details=request.access_auth_details,
                    connected_account=request.connected_account,
                    message="",
                    message_source=message_sources
                )
                return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
            else:
                return ResponseMeta(meta_done=False, meta_message="Invalid Action Requested.")

# find the action
# send the request to particular action
# wait for the action response
# send account assistant message
