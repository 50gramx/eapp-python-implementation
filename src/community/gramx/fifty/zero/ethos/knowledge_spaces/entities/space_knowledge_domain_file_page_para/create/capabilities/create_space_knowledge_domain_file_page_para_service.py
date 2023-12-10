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
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.create_space_knowledge_domain_file_page_para_pb2_grpc import \
    CreateSpaceKnowledgeDomainFilePageParaServiceServicer

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.access.consumers.access_space_knowledge_domain_file_page_consumer import \
    AccessSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace
from support.data_store import DataStore
from support.image_processing.utils import get_image_paragraphs


class CreateSpaceKnowledgeDomainFilePageParaService(CreateSpaceKnowledgeDomainFilePageParaServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(CreateSpaceKnowledgeDomainFilePageParaService, self).__init__()

    def ExtractParasFromPage(self, request, context):
        logging.info("CreateSpaceKnowledgeDomainFilePageParaService:ExtractParasFromPage")
        page_access_consumer = AccessSpaceKnowledgeDomainFilePageConsumer
        validation_done, validation_message = page_access_consumer.validate_space_knowledge_domain_file_page_services(
            request)
        meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return meta
        else:
            page = request.space_knowledge_domain_file_page
            file = page.space_knowledge_domain_file
            domain = file.space_knowledge_domain
            knowledge = domain.space_knowledge
            # download the page from data store
            data_store_client = DataStore()
            data_store_client.download_space_knowledge_domain_file_page(space_knowledge_domain_file_page=page)
            tmp_page_filepath = data_store_client.get_tmp_page_filepath(page=page)
            domain_knowledge_space = DomainKnowledgeSpace(space_knowledge_id=knowledge.space_knowledge_id,
                                                          space_knowledge_domain_id=domain.space_knowledge_domain_id)
            # get the paras
            for page_contour_dims, para_text in get_image_paragraphs(tmp_page_filepath):
                para_id = domain_knowledge_space.add_new_para(page_id=page.space_knowledge_domain_file_page_id,
                                                              contour_dims=page_contour_dims)
                domain_knowledge_space.add_new_para_text(para_id=para_id, para_text=para_text)
            # delete the temp page
            data_store_client.delete_tmp_page(page=page)
            return meta


def save_para_to_dict(path):
    paras_dict = {}
    for index, page_contour_dims, para_text in enumerate(get_image_paragraphs(path)):
        paras_dict[index] = {
            "page_contour_dims": page_contour_dims,
            "para_text": para_text
        }
    return paras_dict
