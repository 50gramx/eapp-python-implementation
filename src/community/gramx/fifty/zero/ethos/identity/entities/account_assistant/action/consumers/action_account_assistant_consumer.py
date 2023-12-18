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
from ethos.elint.entities.account_assistant_pb2 import AccountAssistantConnectedAccount
from ethos.elint.services.product.identity.account_assistant.access_account_assistant_pb2 import \
    AccountAssistantServicesAccessAuthDetails
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2 import \
    ActOnAccountMessageRequest
from ethos.elint.services.product.identity.account_assistant.action_account_assistant_pb2_grpc import \
    ActionAccountAssistantServiceStub


class ActionAccountAssistantConsumer:

    @staticmethod
    async def act_on_account_message(access_auth_details: AccountAssistantServicesAccessAuthDetails,
                                     space_knowledge_action,
                                     connected_account: AccountAssistantConnectedAccount, message):
        aio_grpc_host = os.environ['ERPC_AIO_HOST']
        aio_grpc_port = os.environ['ERPC_AIO_PORT']
        aio_host_ip = "{host}:{port}".format(host=aio_grpc_host, port=aio_grpc_port)

        request = ActOnAccountMessageRequest(
            access_auth_details=access_auth_details,
            space_knowledge_action=space_knowledge_action,
            connected_account=connected_account,
            message=message
        )
        async with grpc.aio.insecure_channel(aio_host_ip) as channel:
            stub = ActionAccountAssistantServiceStub(channel)
            response = await stub.ActOnAccountMessage(request)
        logging.info(f"act_on_account_message client, Response Received: {response}")
