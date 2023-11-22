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
import datetime
import json
import logging
import math
import os

import stripe
from ethos.elint.entities.account_pb2 import AccountPayInCardDetails
from ethos.elint.entities.generic_pb2 import ResponseMeta
from ethos.elint.services.product.identity.account.pay_in_account_pb2 import AccountPayInPublishableKey, \
    AccountPayInAccessKey, ListAllCardsResponse, SaveCardResponse, AccountEthosCoinBalanceResponse, \
    CreditAccountEthosCoinBalanceRequest, \
    VerifyAccountOpenGalaxyPlayStoreSubscriptionChargeRequest, CreateAccountOpenGalaxyTierSubscriptionRequest, \
    VerifyAccountEthosCoinBalanceAdditionRequest
from ethos.elint.services.product.identity.account.pay_in_account_pb2_grpc import PayInAccountServiceServicer
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from grpc import StatusCode

from application_context import ApplicationContext
from community.gramx.fifty.zero.ethos.identity.models.pay_in_models import add_new_account_pay_in, get_account_pay_in_id
from community.gramx.fifty.zero.ethos.identity.services_caller.account_service_caller import \
    validate_account_services_caller
from support.application.tracing import trace_rpc
from support.helper_functions import get_future_timestamp, get_current_timestamp, format_iso_string_to_timestamp, \
    format_timestamp_to_datetime, format_datetime_to_iso_string


class PayInAccountService(PayInAccountServiceServicer):
    def __init__(self):
        super(PayInAccountService, self).__init__()
        stripe.api_key = os.environ['STRIPE_API_KEY']
        self.ethoscoin_price_inr = 1.520408163  # EthosCoin Price With Stripe Taxes
        self.open_galaxy_tier_plans = {
            0: {
                "price_api": "price_1JAVQkF89FbkqSMdPfnZ0rKB",
                # "price_api": "price_1J9dgOF89FbkqSMd2ircLWjC",
                "ethoscoin": 0.1,
                "play_store_subscription_id": "50gramx.subscribe.tier.free",
                "closed_domain_launch_per_month": 1,
                "closed_domain_page_learning_per_month": 5,
                "closed_domain_learning_speed_x": 1,
                "open_inference_per_day": 0,
                "closed_inference_per_day": 2
            },
            1: {
                "price_api": "price_1JAVSVF89FbkqSMd43p6lENq",
                # "price_api": "price_1JAoehF89FbkqSMdWTZbz8WJ",
                "ethoscoin": 287.919463,
                "play_store_subscription_id": "50gramx.space.tier.basic",
                "closed_domain_launch_per_month": 2,
                "closed_domain_page_learning_per_month": 50,
                "closed_domain_learning_speed_x": 50,
                "open_inference_per_day": 2,
                "closed_inference_per_day": 8
            },
            2: {
                "price_api": "price_1JAVTGF89FbkqSMd7RyCtbRd",
                # "price_api": "price_1JAofBF89FbkqSMdHHtho5lc",
                "ethoscoin": 1150.33557,
                "play_store_subscription_id": "50gramx.space.tier.standard",
                "closed_domain_launch_per_month": 4,
                "closed_domain_page_learning_per_month": 500,
                "closed_domain_learning_speed_x": 300,
                "open_inference_per_day": 8,
                "closed_inference_per_day": 32
            },
            3: {
                "price_api": "price_1JAVU9F89FbkqSMd60ftIwgN",
                # "price_api": "price_1JAofZF89FbkqSMdCPdEY4C1",
                "ethoscoin": 4602.01342,
                "play_store_subscription_id": "50gramx.space.tier.professional",
                "closed_domain_launch_per_month": 8,
                "closed_domain_page_learning_per_month": 5000,
                "closed_domain_learning_speed_x": 800,
                "open_inference_per_day": 32,
                "closed_inference_per_day": 64
            }
        }
        self.add_ethoscoin_slabs = {
            0: {
                "ethoscoin": 100,
                "play_store_product_id": "50gramx.add.ethoscoin.100",
            },
            1: {
                "ethoscoin": 200,
                "play_store_product_id": "50gramx.add.ethoscoin.200",
            },
            2: {
                "ethoscoin": 400,
                "play_store_product_id": "50gramx.add.ethoscoin.400",
            },
            3: {
                "ethoscoin": 800,
                "play_store_product_id": "50gramx.add.ethoscoin.800",
            },
            4: {
                "ethoscoin": 1600,
                "play_store_product_id": "50gramx.add.ethoscoin.1600",
            },
            5: {
                "ethoscoin": 3200,
                "play_store_product_id": "50gramx.add.ethoscoin.3200",
            },
            6: {
                "ethoscoin": 6400,
                "play_store_product_id": "50gramx.add.ethoscoin.6400",
            },
        }
        self.play_store_package_name = "com.fiftygramx.ethosai"
        self.service_account_credentials = service_account.Credentials.from_service_account_file(
            os.environ['PLAY_STORE_DEVELOPER_ACCOUNT_SERVICES_KEY_PATH'])
        self.play_service_account_services = build("androidpublisher", "v3",
                                                   credentials=self.service_account_credentials)
        self.account_ethoscoin_charges = {
            "closed_domain_launch": {
                "ethoscoin": 50,
                "price_api": "price_1JGLZlF89FbkqSMdtD7FQvyX",
            },
            "closed_domain_page_learning": {
                "tier": {
                    0: {
                        "price_api": "price_1JGLe3F89FbkqSMdyWnKVtSs",
                        "ethoscoin": 0.5033557047,
                    },
                    1: {
                        "price_api": "price_1JGLe3F89FbkqSMdFoa5Dm5Q",
                        "ethoscoin": 0.4026845638,
                    },
                    2: {
                        "price_api": "price_1JGLe3F89FbkqSMdvGgXji27",
                        "ethoscoin": 0.3355704698,
                    },
                    3: {
                        "price_api": "price_1JGLe3F89FbkqSMdm7PYzvEl",
                        "ethoscoin": 0.1677852349,
                    },
                }
            },
            "closed_inference": {
                "ethoscoin": 3.355704698,
                "price_api": "price_1JGLmbF89FbkqSMdDraiM01R"
            },
            "open_inference": {
                "ethoscoin": 6.711409396,
                "price_api": "price_1JGMHWF89FbkqSMdPhj6jeqB"
            },
        }
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def GetAccountPayInPublishableKey(self, request, context):
        logging.info("PayInAccountService:GetAccountPayInPublishableKey")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return AccountPayInPublishableKey(response_meta=response_meta)
        else:
            return AccountPayInPublishableKey(
                key=os.environ['STRIPE_PUBLISHABLE_API_KEY'],
                response_meta=response_meta
            )

    @trace_rpc()
    def CreateAccountPayIn(self, request, context):
        logging.info("PayInAccountService:CreateAccountPayIn")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return response_meta
        else:
            stripe.api_key = os.environ['STRIPE_API_KEY']
            account = stripe.Customer.create(
                phone=request.account.account_country_code + request.account.account_mobile_number,
                name=request.account.account_first_name + " " + request.account.account_last_name
            )
            add_new_account_pay_in(account_id=request.account.account_id, account_pay_id=account.id)
            return response_meta

    @trace_rpc()
    def GetAccountPayInAccessKey(self, request, context):
        logging.info("PayInAccountService:GetAccountPayInAccessKey")
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

    @trace_rpc()
    def ListAllCards(self, request, context):
        logging.info("PayInAccountService:ListAllCards")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return ListAllCardsResponse(response_meta=response_meta)
        else:
            stripe.api_key = os.environ['STRIPE_API_KEY']
            list_object = stripe.Customer.list_sources(
                get_account_pay_in_id(
                    account_id=request.account.account_id
                ),
                object="card",
                limit=10,
            )
            return ListAllCardsResponse(
                account_pay_in_cards=[
                    AccountPayInCardDetails(
                        card_id=card_data.get("id", ""),
                        brand=card_data.get("brand", ""),
                        country=card_data.get("country", ""),
                        expiry_month=card_data.get("exp_month", 0),
                        expiry_year=card_data.get("exp_year", 0),
                        fingerprint=card_data.get("fingerprint", ""),
                        funding=card_data.get("funding", ""),
                        last_4_digits=card_data.get("last4", "")
                    )
                    for card_data in list_object.data
                ],
                response_meta=response_meta
            )

    @trace_rpc()
    def SaveCard(self, request, context):
        logging.info("PayInAccountService:SaveCard")
        validation_done, validation_message = validate_account_services_caller(request)
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        if validation_done is False:
            return SaveCardResponse(response_meta=response_meta)
        else:
            stripe.api_key = os.environ['STRIPE_API_KEY']
            setup_intent = stripe.SetupIntent.create(
                customer=get_account_pay_in_id(
                    account_id=request.account.account_id
                )
            )
            client_secret = setup_intent.client_secret
            return SaveCardResponse(
                save_card_secret=client_secret,
                response_meta=response_meta
            )

    # ------------------------------------
    # EthosCoin
    # ------------------------------------
    @trace_rpc()
    def AccountEthosCoinBalance(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request)
        logging.info("PayInAccountService:AccountEthosCoinBalance:validation done")
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        logging.info("PayInAccountService:AccountEthosCoinBalance:meta created")
        if validation_done is False:
            logging.info("PayInAccountService:AccountEthosCoinBalance:validation false, returning response")
            return AccountEthosCoinBalanceResponse(response_meta=response_meta)
        else:
            logging.info("PayInAccountService:AccountEthosCoinBalance:validation true, fetching balance")
            list_balance_transactions = stripe.Customer.list_balance_transactions(
                get_account_pay_in_id(request.account.account_id), limit=1).get("data", None)
            logging.info("PayInAccountService:AccountEthosCoinBalance:fetched balance")
            if len(list_balance_transactions) > 0:
                logging.info("PayInAccountService:AccountEthosCoinBalance:balance > 0")
                last_transaction = list_balance_transactions[0]
                logging.info("PayInAccountService:AccountEthosCoinBalance:last transaction computed")
                ending_balance = last_transaction.get("ending_balance", 0)
                logging.info("PayInAccountService:AccountEthosCoinBalance:ending balance computed")
                ethoscoin_balance = ((ending_balance / 100) * -1) / self.ethoscoin_price_inr
                if ethoscoin_balance > 0:
                    logging.info(
                        "PayInAccountService:AccountEthosCoinBalance:balance more than zero, returning response")
                    return AccountEthosCoinBalanceResponse(response_meta=response_meta, balance=ethoscoin_balance)
                elif ethoscoin_balance == 0:
                    logging.info("PayInAccountService:AccountEthosCoinBalance:balance is zero, returning response")
                    return AccountEthosCoinBalanceResponse(
                        response_meta=ResponseMeta(
                            meta_done=validation_done,
                            meta_message="EthosCoin balance is zero. Please add EthosCoin to resume services."
                        ),
                        balance=ethoscoin_balance)
                else:
                    logging.info(
                        "PayInAccountService:AccountEthosCoinBalance:balance is less than zero, returning response")
                    return AccountEthosCoinBalanceResponse(
                        response_meta=ResponseMeta(
                            meta_done=validation_done,
                            meta_message="EthosCoin is due. "
                                         "Please add EthosCoin to balance and resume seamless services."
                        ),
                        balance=ethoscoin_balance)
            else:
                logging.info("PayInAccountService:AccountEthosCoinBalance:no list balance transactions")
                return AccountEthosCoinBalanceResponse(
                    response_meta=ResponseMeta(
                        meta_done=validation_done,
                        meta_message="No EthosCoin transactions found."
                    ),
                    balance=0)

    @trace_rpc()
    def CreditAccountEthosCoinBalance(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        logging.info("PayInAccountService:CreditAccountEthosCoinBalance: validation done")
        if validation_done is False:
            logging.info("PayInAccountService:CreditAccountEthosCoinBalance: validation is false, will return")
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            logging.info("PayInAccountService:CreditAccountEthosCoinBalance: validation is true, will compute")
            customer_id = get_account_pay_in_id(account_id=request.access_auth_details.account.account_id)
            logging.info("PayInAccountService:CreditAccountEthosCoinBalance: got the customer id")
            amount = math.ceil(self.ethoscoin_price_inr * request.add_ethoscoin * 100) * -1
            logging.info("PayInAccountService:CreditAccountEthosCoinBalance: computed the amount")
            try:
                logging.info("PayInAccountService:CreditAccountEthosCoinBalance: will create balance transaction")
                stripe.Customer.create_balance_transaction(
                    customer_id,
                    amount=amount,
                    currency=request.account_currency,
                    metadata={
                        "play_store_subscription_id": request.play_store_subscription_id,
                        "google_play_purchase_token": request.google_play_purchase_token,
                        "play_store_product_id": request.play_store_product_id,
                    },
                    description=request.description
                )
                logging.info("PayInAccountService:CreditAccountEthosCoinBalance: will return successfully")
                return ResponseMeta(meta_done=True, meta_message="Credited Successfully.")
            except Exception as e:
                logging.info(f"PayInAccountService:CreditAccountEthosCoinBalance: will return false for exception: {e}")
                return ResponseMeta(meta_done=False, meta_message="Something went wrong.")

    # ------------------------------------
    # Play Store Subscriptions
    # ------------------------------------
    @trace_rpc()
    def CreateAccountOpenGalaxyTierSubscription(self, request, context):
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: validation done")
        response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: meta created")
        ethoscoin_balance_response = ApplicationContext.pay_in_account_service_stub().AccountEthosCoinBalance(
            request.access_auth_details)
        logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: fetched balance")
        customer_id = get_account_pay_in_id(account_id=request.access_auth_details.account.account_id)
        logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: fetched customer id")
        if ethoscoin_balance_response.response_meta.meta_done is False:
            logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: meta is false, returning")
            return response_meta
        else:
            logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: meta is true, will compute")
            if ethoscoin_balance_response.balance >= 0:
                logging.info("PayInAccountService:CreateAccountOpenGalaxyTierSubscription: balance >= 0")
                if ethoscoin_balance_response.balance < self.open_galaxy_tier_plans.get(
                        request.open_galaxy_tier_enum).get("ethoscoin"):
                    logging.info("Subscription failed due to insufficient EthosCoin Balance.")
                    return ResponseMeta(
                        meta_done=False, meta_message="Subscription failed due to insufficient EthosCoin Balance.")
                else:
                    logging.info("creating subscription")
                    metadata = stripe.Subscription.create(
                        customer=customer_id,
                        items=[
                            {"price": self.open_galaxy_tier_plans.get(request.open_galaxy_tier_enum).get("price_api")},
                        ],
                    )
                    logging.info(f"subscription metadata: {metadata}")
                    try:
                        expiry_datetime = format_timestamp_to_datetime(get_current_timestamp()) + datetime.timedelta(
                            days=1)
                        expiry_iso_string = format_datetime_to_iso_string(expiry_datetime)
                        _ = stripe.Customer.modify(
                            customer_id,
                            metadata=
                            {
                                "open_galaxy_tier": request.open_galaxy_tier_enum,
                                "closed_domain_launch_per_month": self.open_galaxy_tier_plans.get(
                                    request.open_galaxy_tier_enum).get("closed_domain_launch_per_month"),
                                "closed_domain_page_learning_per_month": self.open_galaxy_tier_plans.get(
                                    request.open_galaxy_tier_enum).get("closed_domain_page_learning_per_month"),
                                "closed_domain_learning_speed_x": self.open_galaxy_tier_plans.get(
                                    request.open_galaxy_tier_enum).get("closed_domain_learning_speed_x"),
                                "daily_tier_limits_expiry_iso_string": expiry_iso_string,
                                "open_inference_per_day": self.open_galaxy_tier_plans.get(
                                    request.open_galaxy_tier_enum).get("open_inference_per_day"),
                                "closed_inference_per_day": self.open_galaxy_tier_plans.get(
                                    request.open_galaxy_tier_enum).get("closed_inference_per_day"),
                            },
                        )
                        logging.info("Subscribed successfully.")
                        return ResponseMeta(meta_done=True, meta_message="Subscribed successfully.")
                    except Exception as e:
                        logging.info("Subscription failed due to processing issue. Please contact developer.")
                        return ResponseMeta(
                            meta_done=False,
                            meta_message="Subscription failed due to processing issue. Please contact developer.")
            else:
                logging.info("Subscription failed due to negative EthosCoin Balance. Please clear your dues.")
                return ResponseMeta(
                    meta_done=False,
                    meta_message="Subscription failed due to negative EthosCoin Balance. Please clear your dues."
                )

    @trace_rpc()
    def ConfirmAccountOpenGalaxyPlayStoreSubscription(self, request, context):
        try:
            logging.info("ConfirmAccountOpenGalaxyPlayStoreSubscription: Start")
            validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
            if validation_done is False:
                logging.error(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: Validation failed - {validation_message}")
                return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
            else:
                logging.info(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: Validation passed - {validation_message}")
                verify_response = None
                if request.open_galaxy_tier_enum > 0:
                    logging.info(f"ConfirmAccountOpenGalaxyPlayStoreSubscription: tier > 0")
                    verify_response = ApplicationContext.pay_in_account_service_stub(
                    ).VerifyAccountOpenGalaxyPlayStoreSubscriptionCharge(
                        VerifyAccountOpenGalaxyPlayStoreSubscriptionChargeRequest(
                            access_auth_details=request.access_auth_details,
                            open_galaxy_tier_enum=request.open_galaxy_tier_enum,
                            google_play_purchase_token=request.google_play_purchase_token
                        ))
                    logging.info(f"ConfirmAccountOpenGalaxyPlayStoreSubscription: verify_response: {verify_response}")
                if verify_response is not None and verify_response.meta_done is False:
                    logging.info(
                        f"ConfirmAccountOpenGalaxyPlayStoreSubscription: verify_response is not none, will return")
                    return ResponseMeta(meta_done=False, meta_message=verify_response.meta_message)
                logging.info(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: verify_response is not none"
                    f" and meta is true, will call the CreditAccountEthosCoinBalance")
                _ = ApplicationContext.pay_in_account_service_stub().CreditAccountEthosCoinBalance(
                    CreditAccountEthosCoinBalanceRequest(
                        access_auth_details=request.access_auth_details,
                        add_ethoscoin=self.open_galaxy_tier_plans[request.open_galaxy_tier_enum].get("ethoscoin"),
                        account_currency="INR",
                        play_store_subscription_id=self.open_galaxy_tier_plans[request.open_galaxy_tier_enum].get(
                            "play_store_subscription_id"),
                        google_play_purchase_token=request.google_play_purchase_token,
                        description=f"Purchased Open Galaxy Tier {request.open_galaxy_tier_enum} on Play Store"
                    ))
                logging.info(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: will call CreateAccountOpenGalaxyTierSubscription")
                _ = ApplicationContext.pay_in_account_service_stub().CreateAccountOpenGalaxyTierSubscription(
                    CreateAccountOpenGalaxyTierSubscriptionRequest(
                        access_auth_details=request.access_auth_details,
                        open_galaxy_tier_enum=request.open_galaxy_tier_enum
                    )
                )
                logging.info(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: will call ActivateAccountBilling")
                _ = ApplicationContext.create_account_service_stub().ActivateAccountBilling(request.access_auth_details)
                logging.info(
                    f"ConfirmAccountOpenGalaxyPlayStoreSubscription: will return")
                return ResponseMeta(meta_done=True, meta_message="Successfully subscribed.")
        except Exception as e:
            # You might also want to modify the response or set gRPC status to signal the error.
            context.set_code(StatusCode.INTERNAL)
            context.set_details(f"Internal Server Error: {str(e)}")

    @trace_rpc()
    def VerifyAccountOpenGalaxyPlayStoreSubscriptionCharge(self, request, context):
        logging.info("PayInAccountService:VerifyAccountOpenGalaxyPlayStoreSubscriptionCharge")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            try:
                logging.info(f"tier plans: {self.open_galaxy_tier_plans.get(request.open_galaxy_tier_enum)}")
                logging.info(f"play_store_subscription_id: "
                             f"{self.open_galaxy_tier_plans.get(request.open_galaxy_tier_enum).get('play_store_subscription_id')}")
                play_store_subscription_details = self.play_service_account_services.purchases().subscriptions().get(
                    packageName=self.play_store_package_name,
                    subscriptionId=self.open_galaxy_tier_plans.get(request.open_galaxy_tier_enum).get(
                        "play_store_subscription_id"),
                    token=request.google_play_purchase_token
                ).execute()
                # TODO: Check based on purchase states
                # handle IN_GRACE_PERIOD and RESTORED Purchase States
                play_subscription_expiry_time_seconds = int(play_store_subscription_details.get('expiryTimeMillis'))
                if play_subscription_expiry_time_seconds > get_future_timestamp(
                        after_seconds=60 * 60 * 24 * 27).seconds:
                    return ResponseMeta(meta_done=True, meta_message="Successfully verified subscription charge.")
                else:
                    return ResponseMeta(meta_done=False, meta_message="Subscription Expiry time is less than 27 days")
            except HttpError as http_error:
                return ResponseMeta(meta_done=False, meta_message=http_error.error_details)

    # Add EthosCoin Balance
    @trace_rpc()
    def ConfirmAccountEthosCoinBalanceAddition(self, request, context):
        logging.info("PayInAccountService:ConfirmAccountEthosCoinBalanceAddition")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            verify_response = ApplicationContext.pay_in_account_service_stub(
            ).VerifyAccountEthosCoinBalanceAddition(
                VerifyAccountEthosCoinBalanceAdditionRequest(
                    access_auth_details=request.access_auth_details,
                    add_ethos_coin_enum=request.add_ethos_coin_enum,
                    google_play_purchase_token=request.google_play_purchase_token
                ))
            if verify_response.meta_done is False:
                return ResponseMeta(meta_done=False, meta_message=verify_response.meta_message)
            add_ethoscoin = self.add_ethoscoin_slabs[request.add_ethos_coin_enum].get("ethoscoin")
            _ = ApplicationContext.pay_in_account_service_stub().CreditAccountEthosCoinBalance(
                CreditAccountEthosCoinBalanceRequest(
                    access_auth_details=request.access_auth_details,
                    add_ethoscoin=add_ethoscoin,
                    account_currency="INR",
                    google_play_purchase_token=request.google_play_purchase_token,
                    description=f"Added {add_ethoscoin} EthosCoin on Play Store",
                    play_store_product_id=self.add_ethoscoin_slabs[request.add_ethos_coin_enum].get(
                        "play_store_product_id")
                ))
            return ResponseMeta(meta_done=True, meta_message=f"Successfully Added {add_ethoscoin} EthosCoin.")

    @trace_rpc()
    def VerifyAccountEthosCoinBalanceAddition(self, request, context):
        logging.info("PayInAccountService:VerifyAccountEthosCoinBalanceAddition")
        validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            try:
                play_store_purchase_details = self.play_service_account_services.purchases().products().get(
                    packageName=self.play_store_package_name,
                    productId=self.add_ethoscoin_slabs.get(request.add_ethos_coin_enum).get("play_store_product_id"),
                    token=request.google_play_purchase_token
                ).execute()
                logging.info(f"play_store_purchase_details: {play_store_purchase_details}")
                play_store_purchase_state = int(play_store_purchase_details.get('purchaseState'))
                # https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products#ProductPurchase
                if play_store_purchase_state == 0:  # PURCHASED
                    return ResponseMeta(meta_done=True, meta_message="Successfully Added EthosCoin.")
                elif play_store_purchase_state == 1:  # CANCELLED
                    return ResponseMeta(meta_done=False, meta_message="Cancelled Adding EthosCoin.")
                elif play_store_purchase_state == 2:  # PENDING
                    return ResponseMeta(meta_done=False, meta_message="Purchase Pending.")
            except HttpError as http_error:
                return ResponseMeta(meta_done=False, meta_message=http_error.error_details)

    # call this at the first access of the day to
    # todo: later on at check to subscription status if necessary
    @trace_rpc()
    def UpdateAccountRemainingOpenGalaxyTierBenefits(self, request, context):
        logging.info("PayInAccountService:UpdateAccountRemainingOpenGalaxyTierBenefits")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            customer_id = get_account_pay_in_id(account_id=request.account.account_id)
            open_galaxy_tier = stripe.Customer.retrieve(customer_id).metadata.open_galaxy_tier

            daily_tier_limits_expiry_timestamp = format_iso_string_to_timestamp(
                stripe.Customer.retrieve(customer_id).metadata.daily_tier_limits_expiry_iso_string)
            current_timestamp = get_current_timestamp()

            if current_timestamp.seconds > daily_tier_limits_expiry_timestamp.seconds:
                expiry_datetime = format_timestamp_to_datetime(current_timestamp) + datetime.timedelta(days=1)
                expiry_iso_string = format_datetime_to_iso_string(expiry_datetime)
                stripe.Customer.modify(
                    customer_id,
                    metadata=
                    {
                        "daily_tier_limits_expiry_iso_string": expiry_iso_string,
                        "open_inference_per_day": self.open_galaxy_tier_plans.get(
                            open_galaxy_tier).get("open_inference_per_day"),
                        "closed_inference_per_day": self.open_galaxy_tier_plans.get(
                            open_galaxy_tier).get("closed_inference_per_day"),
                    },
                )
                return ResponseMeta(meta_done=True, meta_message="Daily tier limits successfully updated.")
            else:
                return ResponseMeta(meta_done=True, meta_message="Daily tier limits already updated.")

    @trace_rpc()
    def IsTierBenefitsRemainingForClosedDomainLaunchPerMonth(self, request, context):
        logging.info("PayInAccountService:IsTierBenefitsRemainingForClosedDomainLaunchPerMonth")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            customer_id = get_account_pay_in_id(account_id=request.account.account_id)
            closed_domain_launch_per_month = int(stripe.Customer.retrieve(
                customer_id).metadata.closed_domain_launch_per_month)
            if closed_domain_launch_per_month > 0:
                return ResponseMeta(
                    meta_done=True,
                    meta_message=f"{closed_domain_launch_per_month} Closed Domain Launch remaining for current month"
                )
            else:
                return ResponseMeta(
                    meta_done=False,
                    meta_message=f"No Closed Domain Launch remaining for current month"
                )

    @trace_rpc()
    def IsTierBenefitsRemainingForClosedDomainPageLearningPerMonth(self, request, context):
        logging.info("PayInAccountService:IsTierBenefitsRemainingForClosedDomainPageLearningPerMonth")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            customer_id = get_account_pay_in_id(account_id=request.account.account_id)
            closed_domain_page_learning_per_month = int(stripe.Customer.retrieve(
                customer_id).metadata.closed_domain_page_learning_per_month)
            if closed_domain_page_learning_per_month > 0:
                return ResponseMeta(
                    meta_done=True,
                    meta_message=f"{closed_domain_page_learning_per_month} "
                                 f"Closed Domain Page Learning remaining for current month"
                )
            else:
                return ResponseMeta(
                    meta_done=False,
                    meta_message=f"No Closed Domain Page Learning remaining for current month"
                )

    @trace_rpc()
    def IsTierBenefitsRemainingForClosedDomainInferencePerDay(self, request, context):
        logging.info("PayInAccountService:IsTierBenefitsRemainingForClosedDomainInferencePerDay")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            customer_id = get_account_pay_in_id(account_id=request.account.account_id)
            closed_inference_per_day = int(stripe.Customer.retrieve(
                customer_id).metadata.closed_inference_per_day)
            if closed_inference_per_day > 0:
                return ResponseMeta(
                    meta_done=True,
                    meta_message=f"{closed_inference_per_day} Closed Domain Inference remaining for current day"
                )
            else:
                return ResponseMeta(
                    meta_done=False,
                    meta_message=f"No Closed Domain Inference remaining for current day"
                )

    @trace_rpc()
    def IsTierBenefitsRemainingForOpenDomainInferencePerDay(self, request, context):
        logging.info("PayInAccountService:IsTierBenefitsRemainingForOpenDomainInferencePerDay")
        validation_done, validation_message = validate_account_services_caller(request)
        if validation_done is False:
            return ResponseMeta(meta_done=validation_done, meta_message=validation_message)
        else:
            customer_id = get_account_pay_in_id(account_id=request.account.account_id)
            open_inference_per_day = int(stripe.Customer.retrieve(
                customer_id).metadata.open_inference_per_day)
            if open_inference_per_day > 0:
                return ResponseMeta(
                    meta_done=True,
                    meta_message=f"{open_inference_per_day} Open Domain Inference remaining for current day"
                )
            else:
                return ResponseMeta(
                    meta_done=False,
                    meta_message=f"No Open Domain Inference remaining for current day"
                )

    # TODO: VerifyAccountPlayStoreEthosCoinCharge and what follows
    #
    # def VerifyAccountPlayStoreEthosCoinCharge(self, request, context):
    #     logging.info("PayInAccountService:VerifyPlayStoreEthosCoinCharge")
    #     validation_done, validation_message = validate_account_services_caller(request.access_auth_details)
    #     response_meta = ResponseMeta(meta_done=validation_done, meta_message=validation_message)
    #     result = self.play_service_account_services.purchases().products().get(
    #         packageName=self.play_store_package_name,
    #         productId=self.add_ethoscoin_slabs.get(request.add_ethoscoin_enum),
    #         token=purchase_token
    #     ).execute()

    # Account EthosCoin Charges
    @trace_rpc()
    def ChargeForClosedDomainLaunch(self, request, context):
        logging.info("PayInAccountService:ChargeForClosedDomainLaunch")
        validation_response = ApplicationContext.access_space_knowledge_service_stub().ValidateSpaceKnowledgeServices(
            request)
        if validation_response.space_knowledge_services_access_validation_done is False:
            return ResponseMeta(meta_done=False,
                                meta_message=validation_response.space_knowledge_services_access_validation_message)
        else:
            # Get the space from space knowledge services access auth details
            space = request.space_knowledge.space
            if space.space_entity_type != 0:
                return ResponseMeta(
                    meta_done=False,
                    meta_message="Launch Domain requested by unauthorised entity. This action will be reported.")
            else:
                account_id = space.space_admin_id
                customer_id = get_account_pay_in_id(account_id=account_id)
                # check if free with tier limits
                tier_closed_domain_launch_per_month = int(stripe.Customer.retrieve(
                    customer_id).metadata.closed_domain_launch_per_month)
                if tier_closed_domain_launch_per_month > 0:
                    # reduce the tier limit for closed knowledge domain launch
                    _ = stripe.Customer.modify(
                        customer_id,
                        metadata=
                        {
                            "closed_domain_launch_per_month": tier_closed_domain_launch_per_month - 1,
                        },
                    )
                    # credit the ethoscoin for one domain launch
                    credit_amount = math.ceil(
                        self.ethoscoin_price_inr * self.account_ethoscoin_charges.get("closed_domain_launch").get(
                            "ethoscoin") * 100) * -1
                    stripe.Customer.create_balance_transaction(
                        customer_id,
                        amount=credit_amount,
                        currency="INR",
                        description="Credits for Closed Knowledge Domain Launch with Tier Benefits"
                    )
                    # charge for the closed knowledge domain launch
                    invoice_item = stripe.InvoiceItem.create(
                        customer=customer_id,
                        price=self.account_ethoscoin_charges.get("closed_domain_launch").get("price_api"))
                    invoice_item.auto_advance = True,
                    invoice_item.charge_automatically = True
                    invoice = stripe.Invoice.create(customer=customer_id)
                    finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)
                    return ResponseMeta(
                        meta_done=True,
                        meta_message="Successfully Invoiced for Closed Knowledge Domain Launch with Tier Benefits")
                else:
                    # check for the available balance
                    list_balance_transactions = stripe.Customer.list_balance_transactions(
                        get_account_pay_in_id(account_id), limit=1).get("data", None)
                    if len(list_balance_transactions) > 0:
                        last_transaction = list_balance_transactions[0]
                        ending_balance = last_transaction.get("ending_balance", 0)
                        ethoscoin_balance = ((ending_balance / 100) * -1) / self.ethoscoin_price_inr
                        # check for available balance is more than equal to required balance
                        if ethoscoin_balance >= self.account_ethoscoin_charges.get("closed_domain_launch").get(
                                "ethoscoin"):
                            # charge for the closed knowledge domain launch
                            invoice_item = stripe.InvoiceItem.create(
                                customer=customer_id,
                                price=self.account_ethoscoin_charges.get("closed_domain_launch").get("price_api"))
                            invoice_item.auto_advance = True,
                            invoice_item.charge_automatically = True
                            invoice = stripe.Invoice.create(customer=customer_id)
                            finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)
                            return ResponseMeta(
                                meta_done=True,
                                meta_message="Successfully charged for Closed Knowledge Domain Launch")
                        else:
                            return ResponseMeta(
                                meta_done=False,
                                meta_message="Insufficient EthosCoin Balance. Please add EthosCoin to launch Domain.")
                    else:
                        return ResponseMeta(meta_done=False, meta_message="No EthosCoin transactions found.")
