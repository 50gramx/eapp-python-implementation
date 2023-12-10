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

from ethos.elint.entities import space_knowledge_domain_file_page_pb2
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain_file.access_space_knowledge_domain_file_pb2 import \
    SpaceKnowledgeDomainFileServicesAccessAuthDetails
from google.protobuf.json_format import Parse

from application_context import ApplicationContext

# get the celery worker
from task_loader import TasksLoader

app = TasksLoader.init_celery_worker()


@app.task(queue="eapp_knowledge_queue")
def extract_file_pages(**kwargs):
    TasksLoader.init_celery_worker_context()  # TODO(amit): Convert this as a decorator
    space_knowledge_domain_file_services_access_auth_details_entity = Parse(
        text=kwargs.get('space_knowledge_domain_file_services_access_auth_details'),
        message=SpaceKnowledgeDomainFileServicesAccessAuthDetails()
    )
    # call the service to extract pages from file
    logging.info("Calling the service: ExtractPagesFromFile")
    create_space_knowledge_domain_file_page_service_stub = ApplicationContext.create_space_knowledge_domain_file_page_service_stub()
    response_generator = create_space_knowledge_domain_file_page_service_stub.ExtractPagesFromFile(
        space_knowledge_domain_file_services_access_auth_details_entity
    )
    for response in response_generator:
        logging.info(response)
    space_knowledge_domain_services_access_auth_details_entity = Parse(
        text=kwargs.get('space_knowledge_domain_services_access_auth_details'),
        message=SpaceKnowledgeDomainServicesAccessAuthDetails()
    )
    logging.info("indexing domain pages... calling the service: LearnDomainForRetriever")
    retriever_knowledge_service_stub = ApplicationContext.retriever_knowledge_service_stub()
    learnt_response = retriever_knowledge_service_stub.LearnDomainForRetriever(
        space_knowledge_domain_services_access_auth_details_entity)
    logging.info(f"{'indexing domain pages done!' if learnt_response.meta_done else 'something went wrong!'}")
    logging.info("indexing domain paras... calling the service: LearnDomainParaForRetriever")
    retriever_knowledge_service_stub = ApplicationContext.retriever_knowledge_service_stub()
    learnt_response = retriever_knowledge_service_stub.LearnDomainParaForRetriever(
        space_knowledge_domain_services_access_auth_details_entity)
    logging.info(f"{'indexing domain paras done!' if learnt_response.meta_done else 'something went wrong!'}")


@app.task(queue="eapp_knowledge_queue")
def extract_page_text(**kwargs):
    TasksLoader.init_celery_worker_context()  # TODO(amit): Convert this as a decorator
    space_knowledge_domain_file_page_entity = Parse(
        text=kwargs.get('space_knowledge_domain_file_page'),
        message=space_knowledge_domain_file_page_pb2.SpaceKnowledgeDomainFilePage()
    )
    # call the service to extract text from page
    logging.info("Calling the service: ExtractTextFromPage")
    stub = ApplicationContext.create_space_knowledge_domain_file_page_service_stub()
    response = stub.ExtractTextFromPage(
        space_knowledge_domain_file_page_entity
    )
    logging.info(f"meta_done: {response.meta_done}, meta_message: {response.meta_message}")
