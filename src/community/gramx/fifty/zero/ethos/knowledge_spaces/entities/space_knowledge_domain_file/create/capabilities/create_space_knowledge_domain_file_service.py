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

import asyncio
import logging
import os

from ethos.elint.services.product.knowledge.space_knowledge_domain_file.create_space_knowledge_domain_file_pb2 import \
    UploadSpaceKnowledgeDomainFileResponse
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.create_space_knowledge_domain_file_pb2_grpc import \
    CreateSpaceKnowledgeDomainFileServiceServicer
from google.protobuf.json_format import MessageToJson

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.consumers.access_space_knowledge_domain_file_consumer import \
    AccessSpaceKnowledgeDomainFileConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.create.consumers.create_space_knowledge_domain_file_page_consumer import \
    CreateSpaceKnowledgeDomainFilePageConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.create.tasks.create_space_knowledge_domain_file_page_task import \
    extract_file_pages
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import DomainKnowledgeSpace, \
    KnowledgeSpace
from support.data_store import DataStore


def save_chunk_to_file(chunk, filename):
    with open(filename, 'wb') as f:
        f.write(chunk.file_buffer)


def save_chunks_to_file(chunks, filename):
    with open(filename, 'ab+') as f:
        for chunk in chunks:
            f.write(chunk.file_buffer)


class CreateSpaceKnowledgeDomainFileService(CreateSpaceKnowledgeDomainFileServiceServicer):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(CreateSpaceKnowledgeDomainFileService, self).__init__()

    def UploadSpaceKnowledgeDomainFile(self, request_iterator, context):
        logging.info("CreateSpaceKnowledgeDomainFileService:UploadSpaceKnowledgeDomainFile invoked.")

        # Flag Variables
        fetch_request_params_done = False
        validate_services_auth_done = False
        create_space_knowledge_domain_file_done = False
        request_file_access_auth_done = False
        first_request_uploaded = False

        # Variables
        first_request = None
        access_auth_details = None
        space_knowledge_domain_file_id = None
        space_knowledge_domain_file_name = None
        space_knowledge_domain_file_size = None
        space_knowledge_domain = None
        space_knowledge_domain_id = None
        space_knowledge_domain_file_extension_type = None
        requested_at = None
        tmp_file_path = None

        while fetch_request_params_done is False:
            logging.info("handling first request...")
            first_request = next(request_iterator)
            # request params
            access_auth_details = first_request.space_knowledge_domain_services_access_auth_details
            space_knowledge_domain_file_name = first_request.space_knowledge_domain_file_name
            space_knowledge_domain_file_size = first_request.space_knowledge_domain_file_size
            space_knowledge_domain = access_auth_details.space_knowledge_domain
            space_knowledge_domain_id = space_knowledge_domain.space_knowledge_domain_id
            space_knowledge_domain_file_extension_type = first_request.space_knowledge_domain_file_extension_type
            requested_at = access_auth_details.requested_at
            fetch_request_params_done = True
            domain_knowledge_space = DomainKnowledgeSpace(
                space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id,
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id
            )

        while validate_services_auth_done is False:
            logging.info("validating services...")
            validation_done, validation_message = AccessSpaceKnowledgeDomainConsumer. \
                validate_space_knowledge_domain_services(access_auth_details)
            if validation_done is False:
                return UploadSpaceKnowledgeDomainFileResponse(
                    space_knowledge_domain_file_upload_done=validation_done,
                    space_knowledge_domain_file_upload_message=validation_message,
                )
            else:
                validate_services_auth_done = True

        while create_space_knowledge_domain_file_done is False:
            logging.info("creating new file object...")
            # create the space knowledge domain file params here
            space_knowledge_domain_file_id = domain_knowledge_space.add_new_file(
                file_name=space_knowledge_domain_file_name,
                file_extension_type=space_knowledge_domain_file_extension_type,
                file_size=space_knowledge_domain_file_size
            )
            create_space_knowledge_domain_file_done = True

        while request_file_access_auth_done is False:
            logging.info("accessing file...")
            space_knowledge_domain_file = domain_knowledge_space.get_file_with_id(
                space_knowledge_domain=space_knowledge_domain,
                file_id=space_knowledge_domain_file_id
            )
            access_done, access_message, file_services_access_auth_details = AccessSpaceKnowledgeDomainFileConsumer.space_knowledge_domain_file_access_token(
                access_auth_details, space_knowledge_domain_file)
            if access_done is False:
                logging.info("file access invalid!")
                return UploadSpaceKnowledgeDomainFileResponse(
                    space_knowledge_domain_file_upload_done=access_done,
                    space_knowledge_domain_file_upload_message=access_message)
            else:
                logging.info("creating new file in data store...")
                # create the space knowledge domain file key in data store
                data_store_client = DataStore()
                data_store_client.create_space_knowledge_domain_file(
                    space_knowledge_domain_file=space_knowledge_domain_file
                )
                tmp_file_path = data_store_client.get_tmp_filepath(file=space_knowledge_domain_file)
                request_file_access_auth_done = True
        while first_request_uploaded is False:  # loop while first request from iterator
            logging.info("saving first request...")
            save_chunk_to_file(first_request, tmp_file_path)
            first_request_uploaded = True
        logging.info("saving request...")
        save_chunks_to_file(request_iterator, tmp_file_path)  # save chunks to file
        uploaded_file_size = os.path.getsize(tmp_file_path)  # uploaded file size
        if not uploaded_file_size < space_knowledge_domain_file_size:
            logging.info("upload done to local. uploading in data store...")
            data_store_client.upload_tmp_file(file=space_knowledge_domain_file)  # upload file to data store
            data_store_client.delete_tmp_file(file=space_knowledge_domain_file)  # delete file from local
            KnowledgeSpace(
                space_knowledge_id=space_knowledge_domain.space_knowledge.space_knowledge_id
            ).update_domain_last_updated_at(
                space_knowledge_domain_id=space_knowledge_domain.space_knowledge_domain_id
            )
            logging.info("upload done. extract_file_pages queued.")
            # TODO: check and complete the task
            create_consumer = CreateSpaceKnowledgeDomainFilePageConsumer
            asyncio.run(
                create_consumer.extract_pages_from_file(
                    file_services_access_auth_details=file_services_access_auth_details,
                    domain_services_access_auth_details=access_auth_details,
                )
            )
            # TODO: check and remove the task
            extract_file_pages.apply_async(kwargs={
                'space_knowledge_domain_file_services_access_auth_details': MessageToJson(
                    file_services_access_auth_details),
                'space_knowledge_domain_services_access_auth_details': MessageToJson(access_auth_details)
            }, queue='eapp_knowledge_queue')  # File added to extract file pages queue
        # space_knowledge_domain_file_services_access_auth_details
        logging.info("yielding response...")
        yield UploadSpaceKnowledgeDomainFileResponse(
            space_knowledge_domain_file_service_access_auth_details=file_services_access_auth_details,
            length=False if uploaded_file_size < space_knowledge_domain_file_size else True,
            space_knowledge_domain_file_upload_done=False,
            space_knowledge_domain_file_upload_message="Upload in progress." if uploaded_file_size < space_knowledge_domain_file_size else "Upload completed."
        )
