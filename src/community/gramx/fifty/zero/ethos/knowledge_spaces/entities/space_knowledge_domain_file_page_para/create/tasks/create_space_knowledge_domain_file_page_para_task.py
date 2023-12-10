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

from ethos.elint.services.product.knowledge.space_knowledge_domain_file_page.access_space_knowledge_domain_file_page_pb2 import \
    SpaceKnowledgeDomainFilePageServicesAccessAuthDetails
from google.protobuf.json_format import Parse

from application_context import ApplicationContext
# get the celery worker
from task_loader import TasksLoader

app = TasksLoader.init_celery_worker()


@app.task(queue="eapp_knowledge_queue")
def extract_page_paras(**kwargs):
    TasksLoader.init_celery_worker_context()  # TODO(amit): Convert this as a decorator
    space_knowledge_domain_file_page_services_access_auth_details_entity = Parse(
        text=kwargs.get('space_knowledge_domain_file_page_services_access_auth_details'),
        message=SpaceKnowledgeDomainFilePageServicesAccessAuthDetails()
    )
    # call the service to extract paras from page
    logging.info("Calling the service: ExtractParasFromPage")
    stub = ApplicationContext.create_space_knowledge_domain_file_page_para_service_stub()
    response_generator = stub.ExtractParasFromPage(
        space_knowledge_domain_file_page_services_access_auth_details_entity
    )
    logging.info(response_generator)
