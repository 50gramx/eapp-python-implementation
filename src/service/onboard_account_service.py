import logging
import os
import uuid

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError

from db_session import DbSession
from ethos.elint.entities.account_pb2 import ClaimAccountResponse
from ethos.elint.services.product.identity.onboard_account_pb2_grpc import OnboardAccountServiceServicer
from helpers.helper_functions import validate_email_dns, get_random_string, mail
from helpers.registry import Registry
from models.account_model import Account

logger = logging.getLogger(__name__)
identity_service_mail_id = os.environ['IDENTITY_MAIL_ID']
claim_account_verification_mail_subject = "Verify your account"
claim_account_verification_mail_body = "Short lived verification code: {0}"

timestamp = Timestamp()


class OnboardAccountService(OnboardAccountServiceServicer):

    def claim_account(self, request, context):
        # Getting the request params
        try:
            account_email_id = request.account_email_id
            requested_at = request.requested_at
        except Exception as err:
            account_email_id = None
            requested_at = None
            logger.error("request, exception: {}".format(str(err)))
        # Some helper flags
        account_claimable = None
        account_validated = None
        account_exists = None

        # Validate email id
        account_validated = validate_email_dns(account_email_id)

        # check account exists in the accounts db
        try:
            if account_validated and account_validated is not None:
                with DbSession.session_scope() as session:
                    # Fetch the records
                    exists_statement = exists().where(Account.account_email_id == account_email_id)
                    result_set = session.query(Account).filter(exists_statement)
                    session.commit()
                    # Verify among the existing users
                    for record in result_set:
                        if record.account_email_id == account_email_id:
                            logging.info(
                                f"Warning: re-onboard req by existing user, {record.account_id} at {requested_at}.")
                            account_exists = True
                    if account_exists is not True and account_exists is None:
                        account_exists = False
        except SQLAlchemyError as err:
            logger.error("SQLAlchemyError {}".format(str(err)))
            context.set_code(grpc.StatusCode.UNKNOWN)

        # Generate the boolean feedback about the claimability
        if account_validated and not account_exists:
            account_claimable = True

        if account_claimable:
            verification_code, code_generated_at = get_random_string(6)
            code_token = str(uuid.uuid4())

            Registry.register_data(code_token, [verification_code, code_generated_at])
            mail_successful = mail(
                from_email=identity_service_mail_id,
                to_email=account_email_id,
                subject=claim_account_verification_mail_subject,
                html_content=claim_account_verification_mail_body.format(verification_code)
            )
            return ClaimAccountResponse(
                account_claimable=account_claimable,
                account_email_id=account_email_id,
                code_token=code_token,
                code_sent_at=timestamp.FromDatetime(code_generated_at)
            )
        else:
            return ClaimAccountResponse(
                account_claimable=account_claimable,
                account_email_id=account_email_id
            )
