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
import os

import grpc
from ethos.elint.entities.space_knowledge_domain_file_page_pb2 import SpaceKnowledgeDomainFilePage
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import \
    SpaceKnowledgeDomainFileServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2_grpc import \
    CreateSpaceKnowledgeDomainFilePageServiceStub

from application_context import ApplicationContext

aio_grpc_host = os.environ['ERPC_AIO_HOST']
aio_grpc_port = os.environ['ERPC_AIO_PORT']
aio_host_ip = "{host}:{port}".format(host=aio_grpc_host, port=aio_grpc_port)


class CreateSpaceKnowledgeDomainFilePageConsumer:

    @staticmethod
    async def extract_pages_from_file(
            file_services_access_auth_details: SpaceKnowledgeDomainFileServicesAccessAuthDetails,
            domain_services_access_auth_details: SpaceKnowledgeDomainServicesAccessAuthDetails,
    ):
        async with grpc.aio.insecure_channel(aio_host_ip) as channel:
            stub = CreateSpaceKnowledgeDomainFilePageServiceStub(channel)
            response_generator = stub.ExtractPagesFromFile(file_services_access_auth_details)
            async for response in response_generator:
                logging.info(f"extract_pages_from_file client, Response Received: {response}")
        # TODO: call rest of the tasks
        logging.info("indexing domain pages... calling the service: LearnDomainForRetriever")
        retriever_knowledge_service_stub = ApplicationContext.retriever_knowledge_service_stub()
        learnt_response = retriever_knowledge_service_stub.LearnDomainForRetriever(
            domain_services_access_auth_details)
        logging.info(f"{'indexing domain pages done!' if learnt_response.meta_done else 'something went wrong!'}")
        logging.info("indexing domain paras... calling the service: LearnDomainParaForRetriever")
        retriever_knowledge_service_stub = ApplicationContext.retriever_knowledge_service_stub()
        learnt_response = retriever_knowledge_service_stub.LearnDomainParaForRetriever(
            domain_services_access_auth_details)
        logging.info(f"{'indexing domain paras done!' if learnt_response.meta_done else 'something went wrong!'}")

    @staticmethod
    async def extract_text_from_page(space_knowledge_domain_file_page: SpaceKnowledgeDomainFilePage):
        async with grpc.aio.insecure_channel(aio_host_ip) as channel:
            stub = CreateSpaceKnowledgeDomainFilePageServiceStub(channel)
            response = await stub.ExtractTextFromPage(space_knowledge_domain_file_page)
        logging.info(f"meta_done: {response.meta_done}, meta_message: {response.meta_message}")
