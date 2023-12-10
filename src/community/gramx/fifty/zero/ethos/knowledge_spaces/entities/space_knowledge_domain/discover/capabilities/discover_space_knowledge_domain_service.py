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
from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain, RankedAnswer
from ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2 import \
    GetAllDomainFilesResponse, GetBestAnswersResponse, FileCountResponse, PageCountResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain.discover_space_knowledge_domain_pb2_grpc import \
    DiscoverSpaceKnowledgeDomainServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace, \
    KnowledgeSpace
from community.gramx.sixty.six.ethos.reader.entities.knowledge.reader.consumers.reader_knowledge_consumer import \
    ReaderKnowledgeConsumer
from community.gramx.sixty.six.ethos.retriever.entities.knowledge.retriever.consumers.retriever_knowledge_consumer import \
    RetrieverKnowledgeConsumer


class DiscoverSpaceKnowledgeDomainService(DiscoverSpaceKnowledgeDomainServiceServicer):
    def __init__(self):
        super(DiscoverSpaceKnowledgeDomainService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAllDomainFiles(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:GetAllDomainFiles invoked.")
        space_knowledge_domain = request.space_knowledge_domain
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request)
        if validation_done is False:
            return GetAllDomainFilesResponse()
        else:
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            files = domain_knowledge_space.get_file_all_existing(space_knowledge_domain=space_knowledge_domain)
            return GetAllDomainFilesResponse(files=files)

    def GetUpdatedDomain(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:GetUpdatedDomain invoked.")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request)
        if validation_done is False:
            return SpaceKnowledgeDomain()
        else:
            ks = KnowledgeSpace(space_knowledge_id=request.space_knowledge_domain.space_knowledge.space_knowledge_id)
            return ks.get_domain_with_id(space_knowledge=request.space_knowledge_domain.space_knowledge,
                                         domain_id=request.space_knowledge_domain.space_knowledge_domain_id)

    def IsDomainEmpty(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:IsDomainEmpty")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            dks = DomainKnowledgeSpace(
                space_knowledge_id=request.space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=request.space_knowledge_domain.space_knowledge_domain_id)
            file_count = dks.get_file_count()
            if file_count > 0:
                return ResponseMeta(meta_done=False, meta_message=f"Domain is not empty, and has {file_count} files.")
            else:
                return ResponseMeta(meta_done=True, meta_message=f"Domain is empty.")

    def GetBestAnswers(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:GetBestAnswers invoked.")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return GetBestAnswersResponse(response_meta=meta)
        else:
            ranked_answers = list()
            _, _, ranked_paras = RetrieverKnowledgeConsumer.retrieve_closest_paras(
                access_auth_details=request.access_auth_details,
                message=request.question,
                retrieve_para_count=request.best_answers_count)
            for ranked_para in ranked_paras:
                _, _, para_answer = ReaderKnowledgeConsumer.read_page_question(
                    access_auth_details=request.access_auth_details,
                    para=ranked_para.para, question=request.question)
                if para_answer.answer != "":
                    space_knowledge_domain = request.access_auth_details.space_knowledge_domain
                    context_id = DomainKnowledgeSpace(
                        space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id,
                        space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id
                    ).add_new_domain_qa_context(
                        question=request.question, answer=para_answer.answer,
                        answer_source_para_id=ranked_para.para.space_knowledge_domain_file_page_para_id
                    )
                    ranked_answer = RankedAnswer(context_id=context_id, para_rank=ranked_para.para_rank,
                                                 answer=para_answer.answer)
                    ranked_answers.append(ranked_answer)
            return GetBestAnswersResponse(ranked_answers=ranked_answers, response_meta=meta)

    def GetFileCount(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:GetFileCount")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request.access_auth_details)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return FileCountResponse(response_meta=response_meta)
        else:
            space_knowledge_domain = request.space_knowledge_domain
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            return FileCountResponse(
                file_count=domain_knowledge_space.get_file_count(),
                response_meta=response_meta
            )

    def GetPageCount(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainService:GetPageCount")
        validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
            request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return PageCountResponse(response_meta=response_meta)
        else:
            space_knowledge_domain = request.space_knowledge_domain
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            return PageCountResponse(
                page_count=domain_knowledge_space.get_page_count(),
                response_meta=response_meta
            )
