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

from ethos.elint.services.product.knowledge.space_knowledge.create_space_knowledge_pb2 import \
    CreateAccountSpaceKnowledgeResponse
from ethos.elint.services.product.knowledge.space_knowledge.create_space_knowledge_pb2_grpc import \
    CreateSpaceKnowledgeServiceServicer

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.base_models import SpaceKnowledge
from community.gramx.fifty.zero.ethos.knowledge_spaces.models.knowledge_space_models import KnowledgeSpace
from support.data_store import DataStore
from support.db_service import add_new_entity
from support.helper_functions import gen_uuid, format_timestamp_to_datetime


class CreateSpaceKnowledgeService(CreateSpaceKnowledgeServiceServicer):
    def __init__(self):
        super(CreateSpaceKnowledgeService, self).__init__()
        self.session_scope = self.__class__.__name__

    def CreateAccountSpaceKnowledge(self, request, context):
        logging.info("CreateSpaceKnowledgeService:CreateAccountSpaceKnowledge invoked.")
        space_service_access_auth_details = request.space_service_access_auth_details
        space_knowledge_name = request.space_knowledge_name
        requested_at = request.requested_at

        # validate the auth details
        access_space_service_stub = ApplicationContext.access_space_service_stub()
        validate_space_services_response = access_space_service_stub.ValidateSpaceServices(
            space_service_access_auth_details)
        # handle the response here
        space_service_access_validation_done = validate_space_services_response. \
            space_service_access_validation_done
        space_service_access_validation_message = validate_space_services_response. \
            space_service_access_validation_message

        if space_service_access_validation_done is False:
            # return without creating a space knowledge
            # create the response here
            create_account_space_knowledge_response = CreateAccountSpaceKnowledgeResponse(
                create_account_space_knowledge_done=space_service_access_validation_done,
                create_account_space_knowledge_message=space_service_access_validation_message
            )
        else:
            # create the space knowledge params here
            space_knowledge_id = gen_uuid()
            space = space_service_access_auth_details.space
            space_knowledge_admin_account_id = space.space_admin_id
            # create the space knowledge here
            new_space_knowledge = SpaceKnowledge(
                space_knowledge_id=space_knowledge_id,
                space_knowledge_name=space_knowledge_name,
                space_knowledge_admin_account_id=space_knowledge_admin_account_id,
                space_id=space.space_id,
                created_at=format_timestamp_to_datetime(requested_at)
            )
            # add the entity to database
            add_new_entity(new_space_knowledge)
            knowledge_space = KnowledgeSpace(space_knowledge_id=space_knowledge_id)
            knowledge_space.setup_knowledge_space()

            # request SpaceKnowledgeToken with access_space_knowledge
            # to generate space_knowledge_services_access_auth_details
            access_space_knowledge_service_stub = ApplicationContext.access_space_knowledge_service_stub()
            access_space_knowledge_token_response = access_space_knowledge_service_stub.SpaceKnowledgeAccessToken(
                space_service_access_auth_details)
            space_knowledge_services_access_auth_details = access_space_knowledge_token_response.space_knowledge_services_access_auth_details

            # create the space knowledge key in data store
            data_store_client = DataStore()
            data_store_client.create_space_knowledge(
                space_knowledge=space_knowledge_services_access_auth_details.space_knowledge)

            # create the response params here
            create_account_space_knowledge_done = True
            create_account_space_knowledge_message = "Space Knowledge successfully created. Thanks."

            # create the response here
            create_account_space_knowledge_response = CreateAccountSpaceKnowledgeResponse(
                space_knowledge_services_access_auth_details=space_knowledge_services_access_auth_details,
                create_account_space_knowledge_done=create_account_space_knowledge_done,
                create_account_space_knowledge_message=create_account_space_knowledge_message
            )
        return create_account_space_knowledge_response
