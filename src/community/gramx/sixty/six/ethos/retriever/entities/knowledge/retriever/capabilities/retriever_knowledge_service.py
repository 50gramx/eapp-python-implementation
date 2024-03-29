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
from ethos.elint.services.cognitive.assist.knowledge.retriever_knowledge_pb2 import ClosestPages, RankedPage, \
    ClosestParas, RankedPara
from ethos.elint.services.cognitive.assist.knowledge.retriever_knowledge_pb2_grpc import \
    RetrieverKnowledgeServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.discover.consumers.discover_space_knowledge_domain_consumer import \
    DiscoverSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.discover.consumers.discover_space_knowledge_domain_file_page_consumer import \
    DiscoverSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.discover.consumers.discover_space_knowledge_domain_file_page_para_consumer import \
    DiscoverSpaceKnowledgeDomainFilePageParaConsumer
from community.gramx.sixty.six.ethos.retriever.entities.knowledge.retriever.drqa.retriever import TfidfDocRanker
from community.gramx.sixty.six.ethos.retriever.entities.knowledge.retriever.drqa.retriever.tfidf_para_ranker import \
    TfidfParaRanker
from community.gramx.sixty.six.ethos.retriever.entities.knowledge.retriever.scripts.retriever.build_tfidf import \
    build_domain_tfidf, build_domain_para_tfidf
from support.data_store import DataStore


class RetrieverKnowledgeService(RetrieverKnowledgeServiceServicer):
    def __init__(self):
        super(RetrieverKnowledgeService, self).__init__()
        self.session_scope = self.__class__.__name__

    def LearnDomainForRetriever(self, request, context):
        logging.info("RetrieverKnowledgeService:LearnDomainForRetriever")
        consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = consumer.validate_space_knowledge_domain_services(
            access_auth_details=request
        )
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            data_store = DataStore()
            # try:
            #     model_last_modified_at = datetime_to_timestamp(data_store.get_object_last_modified(
            #         object_key=_get_space_knowledge_domain_tfidf_key(request.space_knowledge_domain)))
            # except:
            #     logging.info("something went wrong! Probably, model was never created")
            #     model_last_modified_at = None
            # updated_domain = ApplicationContext.discover_space_knowledge_domain_service_stub().GetUpdatedDomain(
            #     request).last_updated_at
            # if (model_last_modified_at is None) or (model_last_modified_at.seconds < updated_domain.seconds):
        build_domain_tfidf(space_knowledge_domain_id=request.space_knowledge_domain.space_knowledge_domain_id,
                           out_dir=data_store.get_tmp_domain_tfidf_path(domain=request.space_knowledge_domain))
        # data_store.upload_tmp_domain_tfidf(domain=request.space_knowledge_domain)
        # else:
        #     return ResponseMeta(meta_done=True, meta_message="No new changes to learn.")
        return ResponseMeta(meta_done=True, meta_message="Learned Successfully.")

    def LearnDomainParaForRetriever(self, request, context):
        logging.info("RetrieverKnowledgeService:LearnDomainParaForRetriever")
        consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = consumer.validate_space_knowledge_domain_services(
            access_auth_details=request
        )
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            data_store = DataStore()
            out_dir = data_store.get_tmp_domain_para_tfidf_path(domain=request.space_knowledge_domain)
            build_domain_para_tfidf(space_knowledge_domain_id=request.space_knowledge_domain.space_knowledge_domain_id,
                                    out_dir=out_dir)
            data_store.upload_tmp_domain_para_tfidf(domain=request.space_knowledge_domain)
            return ResponseMeta(meta_done=True, meta_message="Learned Successfully.")

    def RetrieveClosestPages(self, request, context):
        logging.info("RetrieverKnowledgeService:RetrieveClosestPages")
        consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = consumer.validate_space_knowledge_domain_services(
            access_auth_details=request.access_auth_details
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ClosestPages(response_meta=meta)
        else:
            with TfidfDocRanker(space_knowledge_domain=request.access_auth_details.space_knowledge_domain) as ranker:
                closest_page_ids, closest_page_scores = ranker.closest_docs(request.message,
                                                                            request.retrieve_page_count)
            ranked_pages = []
            for index, closest_page_id in enumerate(closest_page_ids):
                _, _, page = DiscoverSpaceKnowledgeDomainFilePageConsumer.get_page_by_id(
                    access_auth_details=request.access_auth_details,
                    space_knowledge_domain_file_page_id=closest_page_id
                )
                ranked_page = RankedPage(page=page, page_rank=closest_page_scores[index])
                ranked_pages.append(ranked_page)
            return ClosestPages(ranked_pages=ranked_pages, response_meta=meta)

    def RetrieveClosestParas(self, request, context):
        logging.info("RetrieverKnowledgeService:RetrieveClosestParas")
        consumer = AccessSpaceKnowledgeDomainConsumer
        validation_done, validation_message = consumer.validate_space_knowledge_domain_services(
            access_auth_details=request.access_auth_details
        )
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ClosestParas(response_meta=meta)
        else:
            logging.info(f"MESSAGE: {request.message}")
            logging.info(
                f"DEBUG:: Message: {request.message},\n\t"
                f"DomainId: {request.access_auth_details.space_knowledge_domain.space_knowledge_domain_id}, \n\t"
                f"DomainName: {request.access_auth_details.space_knowledge_domain.space_knowledge_domain_name}")
            domain_last_updated_at = DiscoverSpaceKnowledgeDomainConsumer.get_updated_domain(
                access_auth_details=request.access_auth_details
            ).last_updated_at
            with TfidfParaRanker(space_knowledge_domain=request.access_auth_details.space_knowledge_domain,
                                 last_updated_at=domain_last_updated_at) as ranker:
                try:
                    closest_para_ids, closest_para_scores = ranker.closest_docs(request.message,
                                                                                request.retrieve_para_count)
                    logging.info(f"DEBUG:: PARA ID's: {closest_para_ids}")
                except RuntimeError:
                    return ClosestParas(response_meta=meta)
            ranked_paras = []
            for index, closest_para_id in enumerate(closest_para_ids):
                _, _, para = DiscoverSpaceKnowledgeDomainFilePageParaConsumer.get_para_by_id(
                    access_auth_details=request.access_auth_details,
                    space_knowledge_domain_file_page_para_id=closest_para_id
                )
                ranked_para = RankedPara(para=para, para_rank=closest_para_scores[index])
                ranked_paras.append(ranked_para)
            return ClosestParas(ranked_paras=ranked_paras, response_meta=meta)
