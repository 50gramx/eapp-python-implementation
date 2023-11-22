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
from time import time

import grpc
from celery import Celery
from google.protobuf.json_format import Parse

from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2 import \
    ActOnAccountMessageRequest
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    ActionAccountAssistantServiceStub

redis_host = os.environ['EA_ID_REDIS_HOST']
redis_port = os.environ['EA_ID_REDIS_PORT']

conversation_action_app = Celery("conversation_action_tasks", broker=f"redis://{redis_host}:{redis_port}/0")

identity_grpc_host = os.environ['EAPP_SERVICE_IDENTITY_HOST']
identity_grpc_port = os.environ['ERPC_PORT']
identity_host_ip = "{host}:{port}".format(host=identity_grpc_host, port=identity_grpc_port)
identity_common_channel = grpc.insecure_channel(identity_host_ip)
identity_common_channel = grpc.intercept_channel(identity_common_channel)

action_account_assistant_service_stub = ActionAccountAssistantServiceStub(identity_common_channel)


@conversation_action_app.task(queue="eapp_conversation_queue")
def act_on_account_message(
        access_auth_details, connected_account, space_knowledge_action, message):
    tic = time()
    access_auth_details_entity = Parse(text=access_auth_details,
                                       message=AccountAssistantServicesAccessAuthDetails())
    connected_account_entity = Parse(text=connected_account,
                                     message=AccountAssistantConnectedAccount())
    space_knowledge_action_entity = space_knowledge_action
    request = ActOnAccountMessageRequest(
        access_auth_details=access_auth_details_entity,
        space_knowledge_action=space_knowledge_action_entity,
        connected_account=connected_account_entity,
        message=message
    )
    response = action_account_assistant_service_stub.ActOnAccountMessage(request)
    print('-' * 50)
    print(response)
    print('-' * 50)
    return
