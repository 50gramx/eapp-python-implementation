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
from ethos.elint.services.product.action.space_knowledge_action_pb2 import AskQuestionResponse, DomainRankedAnswers
from ethos.elint.services.product.action.space_knowledge_action_pb2_grpc import SpaceKnowledgeActionServiceServicer
from support.session.access_manager import load_remembered_space_knowledge_auth, \
    load_remembered_space_knowledge_domain_auth

from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.access.consumers.access_account_assistant_consumer import \
    AccessAccountAssistantConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.discover.consumers.discover_space_knowledge_consumer import \
    DiscoverSpaceKnowledgeConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.discover.consumers.discover_space_knowledge_domain_consumer import \
    DiscoverSpaceKnowledgeDomainConsumer


class SpaceKnowledgeActionService(SpaceKnowledgeActionServiceServicer):
    def __init__(self):
        super(SpaceKnowledgeActionService, self).__init__()
        self.session_scope = self.__class__.__name__

    def AskQuestion(self, request, context):
        logging.info("SpaceKnowledgeActionService:AskQuestion")
        # validate account assistant access auth
        validation_done, validation_message = AccessAccountAssistantConsumer.validate_account_assistant_services(
            access_auth_details=request.access_auth_details
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AskQuestionResponse(response_meta=meta)
        else:
            logging.info("SpaceKnowledgeActionService:AskQuestion:validation_done")
            if request.ask_particular_domain:
                logging.info("SpaceKnowledgeActionService:AskQuestion:ask_particular_domain")
                # Closed Inference (Particular Domain)
                space_knowledge_domain_access = load_remembered_space_knowledge_domain_auth(
                    account_assistant_auth=request.access_auth_details,
                    space_knowledge_domain=request.space_knowledge_domain)
                _, _, ranked_answers = DiscoverSpaceKnowledgeDomainConsumer.get_best_answers(
                    access_auth_details=space_knowledge_domain_access,
                    best_answers_count=20, question=request.message
                )
                ranked_answers.sort(key=lambda x: x.para_rank, reverse=True)
                return AskQuestionResponse(domains_ranked_answers=[
                    DomainRankedAnswers(space_knowledge_domain=request.space_knowledge_domain,
                                        ranked_answers=ranked_answers)
                ], response_meta=meta)
            else:
                logging.info("SpaceKnowledgeActionService:AskQuestion:Beam Inference")
                # Beam Inference (All Closed Domains)
                _, _, space_knowledge_domains = DiscoverSpaceKnowledgeConsumer.get_space_knowledge_domains(
                    access_auth_details=load_remembered_space_knowledge_auth(request.access_auth_details)
                )
                logging.info("SpaceKnowledgeActionService:AskQuestion:loaded space knowledge domains")
                domains_ranked_answers = list()
                for space_knowledge_domain in space_knowledge_domains:
                    logging.info(
                        f"SpaceKnowledgeActionService:AskQuestion:{space_knowledge_domain.space_knowledge_domain_name}")
                    space_knowledge_domain_access = load_remembered_space_knowledge_domain_auth(
                        account_assistant_auth=request.access_auth_details,
                        space_knowledge_domain=space_knowledge_domain)
                    _, _, ranked_answers = DiscoverSpaceKnowledgeDomainConsumer.get_best_answers(
                        access_auth_details=space_knowledge_domain_access,
                        best_answers_count=20, question=request.message)
                    print(f"Ranked Answers: {ranked_answers}")
                    ranked_answers.sort(key=lambda x: x.para_rank, reverse=True)
                    domains_ranked_answers.append(DomainRankedAnswers(space_knowledge_domain=space_knowledge_domain,
                                                                      ranked_answers=ranked_answers))
                return AskQuestionResponse(domains_ranked_answers=domains_ranked_answers, response_meta=meta)
