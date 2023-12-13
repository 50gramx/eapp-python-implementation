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


import os

import grpc
from celery import Celery
from ethos.elint.services.cognitive.assist.knowledge.retriever_knowledge_pb2_grpc import RetrieverKnowledgeServiceStub
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.create_space_knowledge_domain_file_page_pb2_grpc import \
    CreateSpaceKnowledgeDomainFilePageServiceStub
from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page_para.create_space_knowledge_domain_file_page_para_pb2_grpc import \
    CreateSpaceKnowledgeDomainFilePageParaServiceStub

from support.application.registry import Registry


class TasksLoader(object):

    @staticmethod
    def init_celery_worker():
        redis_host = os.environ['EA_ID_REDIS_HOST']
        redis_port = os.environ['EA_ID_REDIS_PORT']

        app = Celery("tasks", broker=f"redis://{redis_host}:{redis_port}/0")
        app.conf.update(
            task_routes={
                '.tasks.act_on_account_message': {'queue', 'eapp_knowledge_queue'},
                '.tasks.extract_file_pages': {'queue', 'eapp_knowledge_queue'},
                '.tasks.extract_page_paras': {'queue', 'eapp_knowledge_queue'},
                '.tasks.extract_page_text': {'queue', 'eapp_knowledge_queue'},
            },
        )
        return app

    @staticmethod
    def init_celery_worker_context():
        TasksLoader.__init_celery_worker_knowledge_service_stub_context()
        TasksLoader.__init_celery_worker_cognitive_retriever_service_stub_context()

    @staticmethod
    def __init_celery_worker_knowledge_service_stub_context():
        # ---------------------------------------------
        # Knowledge Stubs
        # ---------------------------------------------
        knowledge_grpc_host = os.environ['EAPP_SERVICE_KNOWLEDGE_HOST']
        knowledge_grpc_port = os.environ['EAPP_SERVICE_KNOWLEDGE_PORT']
        knowledge_grpc_certificate_file = os.environ['EAPP_SERVICE_KNOWLEDGE_COMMON_GRPC_EXTERNAL_CERTIFICATE_FILE']

        knowledge_host_ip = "{host}:{port}".format(host=knowledge_grpc_host, port=knowledge_grpc_port)

        knowledge_ssl_credentials = grpc.ssl_channel_credentials(open(knowledge_grpc_certificate_file, 'rb').read())
        knowledge_common_channel = grpc.secure_channel(knowledge_host_ip, knowledge_ssl_credentials)

        knowledge_common_channel = grpc.intercept_channel(knowledge_common_channel)

        create_space_knowledge_domain_file_page_service_stub = CreateSpaceKnowledgeDomainFilePageServiceStub(
            knowledge_common_channel)
        Registry.register_service('create_space_knowledge_domain_file_page_service_stub',
                                  create_space_knowledge_domain_file_page_service_stub)

        create_space_knowledge_domain_file_page_para_service_stub = CreateSpaceKnowledgeDomainFilePageParaServiceStub(
            knowledge_common_channel)
        Registry.register_service('create_space_knowledge_domain_file_page_para_service_stub',
                                  create_space_knowledge_domain_file_page_para_service_stub)

        return

    @staticmethod
    def __init_celery_worker_cognitive_retriever_service_stub_context():
        # ---------------------------------------------
        # Retriever Stubs
        # ---------------------------------------------
        retriever_grpc_host = os.environ['EAPP_SERVICE_RETRIEVER_HOST']
        retriever_grpc_port = os.environ['EAPP_SERVICE_RETRIEVER_PORT']
        retriever_host_ip = "{host}:{port}".format(host=retriever_grpc_host, port=retriever_grpc_port)
        # enable ssl secure channel here
        retriever_common_channel = grpc.insecure_channel(retriever_host_ip)
        retriever_common_channel = grpc.intercept_channel(retriever_common_channel)

        retriever_knowledge_service_stub = RetrieverKnowledgeServiceStub(retriever_common_channel)
        Registry.register_service('retriever_knowledge_service_stub', retriever_knowledge_service_stub)

        return
