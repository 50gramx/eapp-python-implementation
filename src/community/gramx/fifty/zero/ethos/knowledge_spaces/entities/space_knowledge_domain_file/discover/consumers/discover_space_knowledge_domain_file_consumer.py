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
import base64

from ethos.elint.entities import space_knowledge_domain_file_pb2
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import (
    SpaceKnowledgeDomainServicesAccessAuthDetails,
)
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.discover_space_knowledge_domain_file_pb2 import (
    DownloadRequest,
    GetFileByIDRequest,
)

from application_context import ApplicationContext


class DiscoverSpaceKnowledgeDomainFileConsumer:

    @staticmethod
    def get_file_by_id(
        skd_auth: SpaceKnowledgeDomainServicesAccessAuthDetails,
        file_id: str,
    ) -> space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile:
        request = GetFileByIDRequest(skd_auth=skd_auth, file_id=file_id)
        stub = ApplicationContext.discover_space_knowledge_domain_file_service_stub()
        response = stub.GetFileByID(request)
        return response

    @staticmethod
    def download(
        skd_auth: SpaceKnowledgeDomainServicesAccessAuthDetails,
        file: space_knowledge_domain_file_pb2.SpaceKnowledgeDomainFile,
    ) -> list:
        request = DownloadRequest(skd_auth=skd_auth, file=file)
        stub = ApplicationContext.discover_space_knowledge_domain_file_service_stub()
        response_generator = stub.Download(request)
        file_content = []
        for response in response_generator:
            file_content.append(response.file_buffer)

        # Combine all byte chunks into a single bytes object.
        image_bytes = b"".join(file_content)

        # Convert the bytes to a Base64-encoded string.
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        return base64_image
