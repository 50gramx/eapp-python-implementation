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

from ethos.elint.entities.space_knowledge_domain_file_pb2 import (
    SpaceKnowledgeDomainFile,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.discover_space_knowledge_domain_file_pb2 import (
    DownloadResponse,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.discover_space_knowledge_domain_file_pb2_grpc import (
    DiscoverKnowledgeDomainFileServiceServicer,
)

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import (
    AccessSpaceKnowledgeDomainConsumer,
)
from src.community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import (
    DomainKnowledgeSpace,
)
from support.data_store import DataStore


class DiscoverSpaceKnowledgeDomainFileService(
    DiscoverKnowledgeDomainFileServiceServicer
):
    def __init__(self):
        self.session_scope = self.__class__.__name__
        super(DiscoverSpaceKnowledgeDomainFileService, self).__init__()

    def GetFileByID(self, request, context):
        logging.info(f"{self.session_scope}:GetFileByID")
        skd_auth = request.skd_auth
        validation_done, validation_message = (
            AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
                skd_auth
            )
        )
        if validation_done == False:
            return SpaceKnowledgeDomainFile()
        else:
            # get params from request
            skd = skd_auth.space_knowledge_domain
            sk = skd.space_knowledge
            skd_id = skd.space_knowledge_domain_id
            sk_id = sk.space_knowledge_id
            f_id = request.file_id
            # get file by id
            dks = DomainKnowledgeSpace(
                space_knowledge_id=sk_id, space_knowledge_domain_id=skd_id
            )
            f = dks.get_file_with_id(space_knowledge_domain=skd, file_id=f_id)
            # return file
            return f

    def Download(self, request, context):
        logging.info("DiscoverSpaceKnowledgeDomainFileService:Download")
        access_auth_details = request.skd_auth
        validation_done, validation_message = (
            AccessSpaceKnowledgeDomainConsumer.validate_space_knowledge_domain_services(
                access_auth_details
            )
        )
        if validation_done == False:
            return DownloadResponse()
        else:
            # start the process
            file = request.file
            data_store_client = DataStore()
            data_store_client.download_space_knowledge_domain_file(
                space_knowledge_domain_file=file
            )  # loaded the file to local
            local_fp = data_store_client.get_tmp_filepath(file=file)
            # Stream file chunks to the client
            with open(local_fp, "rb") as f:
                while chunk := f.read(1024 * 64):  # Stream in 64KB chunks
                    yield DownloadResponse(file_buffer=chunk)
