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

from ethos.elint.entities.space_knowledge_domain_pb2 import SpaceKnowledgeDomain
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.space.access_space_pb2 import SpaceServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge.access_space_knowledge_pb2 import \
    SpaceKnowledgeServicesAccessAuthDetails
from ethos.elint.services.product.knowledge.space_knowledge_domain.access_space_knowledge_domain_pb2 import \
    SpaceKnowledgeDomainServicesAccessAuthDetails
from google.protobuf.text_format import MessageToString, Parse

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.identity.entities.space.access.consumers.access_space_consumer import \
    AccessSpaceConsumer
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.access.consumers.access_space_knowledge_domain_consumer import \
    AccessSpaceKnowledgeDomainConsumer
from services_caller.space_knowledge_services_caller import space_knowledge_access_token
from support.session.redis_service import get_redis_connector

redis_connector = get_redis_connector()


# ------------------------------------
# Space Access Management
# ------------------------------------

def remember_space_auth(account_assistant_id: str, space_auth: SpaceServicesAccessAuthDetails):
    redis_connector.mset({f"{account_assistant_id}_space_auth": MessageToString(space_auth, as_one_line=True)})
    return


def load_remembered_space_auth(
        account_assistant_auth: AccountAssistantServicesAccessAuthDetails) -> SpaceServicesAccessAuthDetails:
    space_auth = redis_connector.get(f"{account_assistant_auth.account_assistant.account_assistant_id}_space_auth")
    if space_auth is not None:
        remembered_space_auth = Parse(text=space_auth, message=SpaceServicesAccessAuthDetails())
        # remembered_space_auth.requested_at = get_current_timestamp()
        # warn: AttributeError: Assignment not allowed to field "requested_at" in protocol message object
        validate_space_services_response = ApplicationContext.access_space_service_stub().ValidateSpaceServices(
            remembered_space_auth)
        if validate_space_services_response.space_service_access_validation_done:
            return remembered_space_auth
    done, message, space_services_access_auth_details = AccessSpaceConsumer.assist_space_access_token(
        access_auth_details=account_assistant_auth)
    if done is False:
        return SpaceServicesAccessAuthDetails()
    else:
        remember_space_auth(account_assistant_auth.account_assistant.account_assistant_id,
                            space_services_access_auth_details)
        return space_services_access_auth_details


# ------------------------------------
# Space Knowledge Access Management
# ------------------------------------

def remember_space_knowledge_auth(account_assistant_id: str,
                                  space_knowledge_auth: SpaceKnowledgeServicesAccessAuthDetails):
    redis_connector.mset(
        {f"{account_assistant_id}_space_knowledge_auth": MessageToString(space_knowledge_auth, as_one_line=True)})
    return


def load_remembered_space_knowledge_auth(
        account_assistant_auth: AccountAssistantServicesAccessAuthDetails) -> SpaceKnowledgeServicesAccessAuthDetails:
    logging.info("load_remembered_space_knowledge_auth")
    space_knowledge_auth = redis_connector.get(
        f"{account_assistant_auth.account_assistant.account_assistant_id}_space_knowledge_auth")
    if space_knowledge_auth is not None:
        logging.info("space_knowledge_auth is not None")
        remembered_space_knowledge_auth = Parse(text=space_knowledge_auth,
                                                message=SpaceKnowledgeServicesAccessAuthDetails())
        # remembered_space_knowledge_auth.requested_at = get_current_timestamp()
        # warn: AttributeError: Assignment not allowed to field "requested_at" in protocol message object
        validate_space_knowledge_services_response = ApplicationContext.access_space_knowledge_service_stub().ValidateSpaceKnowledgeServices(
            remembered_space_knowledge_auth)
        if validate_space_knowledge_services_response.space_knowledge_services_access_validation_done:
            return remembered_space_knowledge_auth
    logging.info("space_knowledge_auth is None")
    done, message, space_knowledge_services_access_auth_details = space_knowledge_access_token(
        access_auth_details=load_remembered_space_auth(account_assistant_auth))
    if done is False:
        return SpaceKnowledgeServicesAccessAuthDetails()
    else:
        remember_space_knowledge_auth(account_assistant_auth.account_assistant.account_assistant_id,
                                      space_knowledge_services_access_auth_details)
        return space_knowledge_services_access_auth_details


# ------------------------------------
# Space Knowledge Domain Access Management
# ------------------------------------

def remember_space_knowledge_domain_auth(account_assistant_id: str,
                                         space_knowledge_domain_auth: SpaceKnowledgeDomainServicesAccessAuthDetails):
    redis_connector.mset(
        {
            f"{account_assistant_id}_space_knowledge_domain_auth_{space_knowledge_domain_auth.space_knowledge_domain.space_knowledge_domain_id}": MessageToString(
                space_knowledge_domain_auth,
                as_one_line=True)})
    return


def load_remembered_space_knowledge_domain_auth(account_assistant_auth: AccountAssistantServicesAccessAuthDetails,
                                                space_knowledge_domain: SpaceKnowledgeDomain) -> SpaceKnowledgeDomainServicesAccessAuthDetails:
    space_knowledge_domain_auth = redis_connector.get(
        f"{account_assistant_auth.account_assistant.account_assistant_id}_space_knowledge_domain_auth_{space_knowledge_domain.space_knowledge_domain_id}")
    if space_knowledge_domain_auth is not None:
        remembered_space_knowledge_domain_auth = Parse(text=space_knowledge_domain_auth,
                                                       message=SpaceKnowledgeDomainServicesAccessAuthDetails())
        # remembered_space_knowledge_domain_auth.requested_at = get_current_timestamp()
        # warn: AttributeError: Assignment not allowed to field "requested_at" in protocol message object
        validate_space_knowledge_domain_services_response = ApplicationContext.access_space_knowledge_domain_service_stub().ValidateSpaceKnowledgeDomainServices(
            remembered_space_knowledge_domain_auth)
        if validate_space_knowledge_domain_services_response.space_knowledge_domain_services_access_validation_done:
            return remembered_space_knowledge_domain_auth
    space_knowledge_domain_services_access_auth_details, done, message = AccessSpaceKnowledgeDomainConsumer.space_knowledge_domain_access_token(
        access_auth_details=load_remembered_space_knowledge_auth(account_assistant_auth),
        space_knowledge_domain=space_knowledge_domain
    )
    if done is False:
        return SpaceKnowledgeDomainServicesAccessAuthDetails()
    else:
        remember_space_knowledge_domain_auth(account_assistant_auth.account_assistant.account_assistant_id,
                                             space_knowledge_domain_services_access_auth_details)
        return space_knowledge_domain_services_access_auth_details
