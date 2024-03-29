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

from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2 import \
    ExtractPagesFromFileResponse, ExtractTextFromPageResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2_grpc import \
    CreateSpaceKnowledgeDomainFilePageServiceServicer
from google.protobuf.json_format import MessageToJson
from pdf2image import convert_from_path

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.consumers.access_space_knowledge_domain_file_consumer import \
    AccessSpaceKnowledgeDomainFileConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.access.consumers.access_space_knowledge_domain_file_page_consumer import \
    AccessSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.create.consumers.create_space_knowledge_domain_file_page_consumer import \
    CreateSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.create.tasks.create_space_knowledge_domain_file_page_para_task import \
    extract_page_paras
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace
from support.application.tracing import trace_rpc
from support.data_store import DataStore
from support.image_processing.utils import get_page_image_text


class CreateSpaceKnowledgeDomainFilePageService(CreateSpaceKnowledgeDomainFilePageServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(CreateSpaceKnowledgeDomainFilePageService, self).__init__()

    @trace_rpc()
    async def ExtractPagesFromFile(self, request, context):
        logging.info("CreateSpaceKnowledgeDomainFilePageService:ExtractPagesFromFile invoked.")
        validation_done, validation_message = AccessSpaceKnowledgeDomainFileConsumer.validate_space_knowledge_domain_file_services(
            request)
        if validation_done is False:
            yield ExtractPagesFromFileResponse(meta_done=validation_done, meta_message=validation_message)
        else:
            data_store_client = DataStore()
            space_knowledge_domain_file = request.space_knowledge_domain_file
            space_knowledge_domain = space_knowledge_domain_file.space_knowledge_domain
            space_knowledge_id = space_knowledge_domain.space_knowledge.space_knowledge_id
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id)
            data_store_client.download_space_knowledge_domain_file(
                space_knowledge_domain_file=space_knowledge_domain_file)  # load the file to local
            pages = convert_from_path(data_store_client.get_tmp_filepath(file=space_knowledge_domain_file))
            total_pages_count = len(pages)
            for page_num, page in enumerate(pages):
                page_count = page_num + 1
                space_knowledge_domain_file_page_id = domain_knowledge_space.add_new_page(
                    page_count=page_count,
                    file_id=space_knowledge_domain_file.space_knowledge_domain_file_id)  # add page to db
                space_knowledge_domain_file_page = domain_knowledge_space.get_page_with_id(
                    space_knowledge_domain_file=space_knowledge_domain_file,
                    page_id=space_knowledge_domain_file_page_id
                )  # retrieve page from db
                page.save(data_store_client.get_tmp_page_filepath(
                    page=space_knowledge_domain_file_page)
                )  # save page to local
                data_store_client.upload_tmp_page(page=space_knowledge_domain_file_page)  # upload page to data store
                data_store_client.delete_tmp_page(page=space_knowledge_domain_file_page)  # delete page from local
                # warn: expected to work in an event-loop
                await CreateSpaceKnowledgeDomainFilePageConsumer.extract_text_from_page(
                    space_knowledge_domain_file_page=space_knowledge_domain_file_page
                )  # extract text from page
                _, _, file_page_access_auth_details = AccessSpaceKnowledgeDomainFilePageConsumer.space_knowledge_domain_file_page_access_token(
                    access_auth_details=request,
                    space_knowledge_domain_file_page=space_knowledge_domain_file_page)
                extract_page_paras.apply_async(kwargs={
                    'space_knowledge_domain_file_page_services_access_auth_details': (
                        MessageToJson(file_page_access_auth_details))
                }, queue='eapp_knowledge_queue')
                yield ExtractPagesFromFileResponse(
                    total_pages_count=total_pages_count,
                    extracted_pages_count=page_count,
                    meta_done=False if page_count < total_pages_count else True,
                    meta_message="Extracting Pages." if page_count < total_pages_count else "Extraction done."
                )

    @trace_rpc()
    async def ExtractTextFromPage(self, request, context):
        logging.info("CreateSpaceKnowledgeDomainFilePageService:ExtractTextFromPage invoked.")
        page_text = get_page_image_text(request)
        # add the text from the page to domain models
        space_knowledge_id = request.space_knowledge_domain_file.space_knowledge_domain.space_knowledge.space_knowledge_id
        space_knowledge_domain_id = request.space_knowledge_domain_file.space_knowledge_domain.space_knowledge_domain_id
        domain_knowledge_space = DomainKnowledgeSpace(space_knowledge_id=space_knowledge_id,
                                                      space_knowledge_domain_id=space_knowledge_domain_id)
        domain_knowledge_space.add_new_page_text(
            page_id=request.space_knowledge_domain_file_page_id,
            page_text=page_text
        )
        return ExtractTextFromPageResponse(
            meta_done=True,
            meta_message="Successfully extracted text from page."
        )
