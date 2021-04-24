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
import json
import os

import stripe

from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.pay_in_account_pb2 import AccountPayInPublishableKey, \
    AccountPayInAccessKey
from ethos.elint.services.product.identity.account.pay_in_account_pb2_grpc import PayInAccountServiceServicer
from models.pay_in_models import add_new_account_pay_in, get_account_pay_in_id
from services_caller.account_service_caller import validate_account_services_caller


class PayInAccountService(PayInAccountServiceServicer):
    def __init__(self):
        super(PayInAccountService, self).__init__()
        self.session_scope = self.__class__.__name__

    def GetAccountPayInPublishableKey(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountPayInPublishableKey(response_meta=response_meta)
        else:
            return AccountPayInPublishableKey(
                key=os.environ['STRIPE_API_KEY'],
                response_meta=response_meta
            )

    def CreateAccountPayIn(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            stripe.api_key = os.environ['STRIPE_API_KEY']
            account = stripe.Customer.create(
                phone=request.account.account_mobile_number,
                name=request.account.account_first_name + request.account.account_last_name
            )
            add_new_account_pay_in(account_id=request.account.account_id, account_pay_id=account.id)
            return response_meta

    def GetAccountPayInAccessKey(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountPayInAccessKey(response_meta=response_meta)
        else:
            stripe.api_key = os.environ['STRIPE_API_KEY']
            key = stripe.EphemeralKey.create(
                customer=get_account_pay_in_id(
                    account_id=request.account.account_id
                ),
                stripe_version=os.environ['STRIPE_API_VERSION']
            )
            return AccountPayInAccessKey(json_key=json.dumps(key), response_meta=response_meta)
