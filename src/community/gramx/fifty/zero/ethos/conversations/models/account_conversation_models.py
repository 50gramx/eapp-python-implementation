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

from datetime import datetime
from typing import Generator

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
from ethos.elint.services.product.conversation.message.account import receive_account_message_pb2, \
    send_account_message_pb2
from support.helper_functions import gen_uuid, format_datetime_to_timestamp

AccountConversationModels = declarative_base()


# ----------------------------------------
# Account Conversation Models
# ----------------------------------------
class AccountConversations:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.account_assistant_sent_messages_model_name = f"acaasm_{account_id}"
        self.account_assistant_received_messages_model_name = f"acaarm_{account_id}"
        self.account_sent_messages_model_name = f"acasm_{account_id}"
        self.account_received_messages_model_name = f"acarm_{account_id}"
        AccountConversationModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.account_assistant_sent_messages_table = AccountConversationModels.metadata.tables[
                self.account_assistant_sent_messages_model_name]
            self.account_assistant_received_messages_table = AccountConversationModels.metadata.tables[
                self.account_assistant_received_messages_model_name]
            self.account_sent_messages_table = AccountConversationModels.metadata.tables[
                self.account_sent_messages_model_name]
            self.account_received_messages_table = AccountConversationModels.metadata.tables[
                self.account_received_messages_model_name]
        except KeyError:
            self.account_assistant_sent_messages_table = None
            self.account_assistant_received_messages_table = None
            self.account_sent_messages_table = None
            self.account_received_messages_table = None

            # Setup Account Conversations

    def setup_account_conversations(self):
        self.get_account_assistant_sent_messages_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_assistant_received_messages_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_sent_messages_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_received_messages_model().__table__.create(bind=DbSession.get_engine())
        return

    # Account Assistant Sent Messages
    def get_account_assistant_sent_messages_model(self):
        class AccountAssistantSentMessages(AccountConversationModels):
            __tablename__ = self.account_assistant_sent_messages_model_name

            account_assistant_sent_message_id = Column(String(255), primary_key=True)
            account_assistant_id = Column(String(255), nullable=False)
            account_assistant_connection_id = Column(String(255), nullable=False)
            message = Column(String(), nullable=False)
            message_space = Column(Integer, nullable=False)
            message_space_action = Column(Integer, nullable=False)
            sent_at = Column(DateTime(), nullable=False)
            received_at = Column(DateTime(), nullable=True)

        return AccountAssistantSentMessages

    def get_account_assistant_sent_messages_model_name(self):
        return self.account_assistant_sent_messages_model_name

    def add_account_assistant_sent_message(self, account_assistant_id: str, account_assistant_connection_id: str,
                                           message: str, message_space: int, message_space_action: int,
                                           sent_at: datetime) -> str:
        account_assistant_sent_message_id = gen_uuid()
        statement = AccountConversationModels.metadata.tables[
            self.account_assistant_sent_messages_model_name].insert().values(
            account_assistant_sent_message_id=account_assistant_sent_message_id,
            account_assistant_id=account_assistant_id,
            account_assistant_connection_id=account_assistant_connection_id,
            message=message,
            message_space=message_space,
            message_space_action=message_space_action,
            sent_at=sent_at
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return account_assistant_sent_message_id

    def update_account_assistant_sent_message_received_at(self, account_assistant_sent_message_id: str,
                                                          received_at: datetime):
        statement = AccountConversationModels.metadata.tables[
            self.account_assistant_sent_messages_model_name].update().values(
            received_at=received_at
        ).where(
            self.account_assistant_sent_messages_table.c.account_assistant_sent_message_id == account_assistant_sent_message_id)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def get_all_account_connected_account_assistant_sent_messages(
            self, account_assistant_id: str, filter_from_datetime: bool = False, from_datetime: datetime = None
    ) -> Generator[dict, None, None]:
        with DbSession.session_scope() as session:
            if not filter_from_datetime:
                all_account_connected_account_assistant_sent_messages = session.query(
                    self.account_assistant_sent_messages_table
                ).filter(
                    self.account_assistant_sent_messages_table.c.account_assistant_id == account_assistant_id
                ).all()
                total_messages_count = len(all_account_connected_account_assistant_sent_messages)
            else:
                all_account_connected_account_assistant_sent_messages = session.query(
                    self.account_assistant_sent_messages_table
                ).filter(
                    self.account_assistant_sent_messages_table.c.account_assistant_id == account_assistant_id,
                    self.account_assistant_sent_messages_table.c.sent_at >= from_datetime
                ).all()
                total_messages_count = len(all_account_connected_account_assistant_sent_messages)
            for index, sent_message in enumerate(all_account_connected_account_assistant_sent_messages):
                if sent_message.received_at is not None:
                    yield {
                        'message': send_account_message_pb2.AccountAssistantSentMessage(
                            account_assistant_sent_message_id=sent_message.account_assistant_sent_message_id,
                            account_assistant_id=sent_message.account_assistant_id,
                            account_assistant_connection_id=sent_message.account_assistant_connection_id,
                            message=sent_message.message,
                            message_space=sent_message.message_space,
                            message_space_action=sent_message.message_space_action,
                            sent_at=format_datetime_to_timestamp(sent_message.sent_at),
                            received_at=format_datetime_to_timestamp(sent_message.received_at)
                        ),
                        'progress': (index / total_messages_count)
                    }
                else:
                    yield {
                        'message': send_account_message_pb2.AccountAssistantSentMessage(
                            account_assistant_sent_message_id=sent_message.account_assistant_sent_message_id,
                            account_assistant_id=sent_message.account_assistant_id,
                            account_assistant_connection_id=sent_message.account_assistant_connection_id,
                            message=sent_message.message,
                            message_space=sent_message.message_space,
                            message_space_action=sent_message.message_space_action,
                            sent_at=format_datetime_to_timestamp(sent_message.sent_at)
                        ),
                        'progress': (index / total_messages_count)
                    }

    def get_account_assistant_sent_messages_count(self) -> int:
        with DbSession.session_scope() as session:
            sent_messages_count = session.query(self.account_assistant_sent_messages_table).count()
            return sent_messages_count

    def get_account_assistant_last_sent_message(
            self,
            account_assistant_id: str) -> send_account_message_pb2.AccountAssistantSentMessage:
        with DbSession.session_scope() as session:
            last_sent_message = session.query(
                self.account_assistant_sent_messages_table
            ).filter(
                self.account_assistant_sent_messages_table.c.account_assistant_id == account_assistant_id
            ).order_by(
                self.account_assistant_sent_messages_table.c.sent_at.desc()
            ).first()
            if last_sent_message is not None:
                if last_sent_message.received_at is not None:
                    return send_account_message_pb2.AccountAssistantSentMessage(
                        account_assistant_sent_message_id=last_sent_message.account_assistant_sent_message_id,
                        account_assistant_id=last_sent_message.account_assistant_id,
                        account_assistant_connection_id=last_sent_message.account_assistant_connection_id,
                        message=last_sent_message.message,
                        message_space=last_sent_message.message_space,
                        message_space_action=last_sent_message.message_space_action,
                        sent_at=format_datetime_to_timestamp(last_sent_message.sent_at),
                        received_at=format_datetime_to_timestamp(last_sent_message.received_at)
                    )
                else:
                    return send_account_message_pb2.AccountAssistantSentMessage(
                        account_assistant_sent_message_id=last_sent_message.account_assistant_sent_message_id,
                        account_assistant_id=last_sent_message.account_assistant_id,
                        account_assistant_connection_id=last_sent_message.account_assistant_connection_id,
                        message=last_sent_message.message,
                        message_space=last_sent_message.message_space,
                        message_space_action=last_sent_message.message_space_action,
                        sent_at=format_datetime_to_timestamp(last_sent_message.sent_at)
                    )
            else:
                return send_account_message_pb2.AccountAssistantSentMessage()

    # TODO: Verification pending
    def get_sent_messages_account_assistant_ids(self) -> [str]:
        with DbSession.session_scope() as session:
            sent_messages_account_assistant_ids = []
            for distinct_sent_messages_account_assistant_id in session.query(
                    self.account_assistant_sent_messages_table.c.account_assistant_id
            ).distinct():
                sent_messages_account_assistant_ids.append(
                    distinct_sent_messages_account_assistant_id.account_assistant_id)
            return sent_messages_account_assistant_ids

    # Account Assistant Received Messages
    def get_account_assistant_received_messages_model(self):
        class AccountAssistantReceivedMessages(AccountConversationModels):
            __tablename__ = self.account_assistant_received_messages_model_name

            account_assistant_received_message_id = Column(String(), primary_key=True)
            account_assistant_id = Column(String(255), nullable=False)
            account_assistant_connection_id = Column(String(255), nullable=False)
            message = Column(String())
            message_source_space_id = Column(String(255))
            message_source_space_type_id = Column(String(255))
            message_source_space_domain_id = Column(String(255))
            message_source_space_domain_action = Column(Integer)
            message_source_space_domain_action_context_id = Column(String(255))
            received_at = Column(DateTime())

        return AccountAssistantReceivedMessages

    def get_account_assistant_received_messages_model_name(self):
        return self.account_assistant_received_messages_model_name

    def add_account_assistant_received_message(self, account_assistant_received_message_id: str,
                                               account_assistant_id: str,
                                               account_assistant_connection_id: str,
                                               message: str, message_source_space_id: str,
                                               message_source_space_type_id: str,
                                               message_source_space_domain_id: str,
                                               message_source_space_domain_action: int,
                                               message_source_space_domain_action_context_id: str,
                                               received_at: datetime):
        statement = AccountConversationModels.metadata.tables[
            self.account_assistant_received_messages_model_name].insert().values(
            account_assistant_received_message_id=account_assistant_received_message_id,
            account_assistant_id=account_assistant_id,
            account_assistant_connection_id=account_assistant_connection_id,
            message=message,
            message_source_space_id=message_source_space_id,
            message_source_space_type_id=message_source_space_type_id,
            message_source_space_domain_id=message_source_space_domain_id,
            message_source_space_domain_action=message_source_space_domain_action,
            message_source_space_domain_action_context_id=message_source_space_domain_action_context_id,
            received_at=received_at
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def get_account_assistant_received_message_received_at(self,
                                                           account_assistant_received_message_id: str) -> datetime:
        with DbSession.session_scope() as session:
            account_assistant_received_message = session.query(
                self.account_assistant_received_messages_table).filter(
                self.account_assistant_received_messages_table.c.account_assistant_received_message_id == account_assistant_received_message_id
            ).first()
            return account_assistant_received_message.received_at

    def get_all_account_connected_account_assistant_received_messages(
            self, account_assistant_id: str, filter_from_datetime: bool = False, from_datetime: datetime = None
    ) -> Generator[dict, None, None]:
        with DbSession.session_scope() as session:
            if not filter_from_datetime:
                all_account_connected_account_assistant_received_messages = session.query(
                    self.account_assistant_received_messages_table
                ).filter(
                    self.account_assistant_received_messages_table.c.account_assistant_id == account_assistant_id
                ).all()
                total_messages_count = len(all_account_connected_account_assistant_received_messages)
            else:
                all_account_connected_account_assistant_received_messages = session.query(
                    self.account_assistant_received_messages_table
                ).filter(
                    self.account_assistant_received_messages_table.c.account_assistant_id == account_assistant_id,
                    self.account_assistant_received_messages_table.c.received_at >= from_datetime
                ).all()
                total_messages_count = len(all_account_connected_account_assistant_received_messages)
            for index, received_message in enumerate(all_account_connected_account_assistant_received_messages):
                yield {
                    'message': receive_account_message_pb2.AccountAssistantReceivedMessage(
                        account_assistant_received_message_id=received_message.account_assistant_received_message_id,
                        account_assistant_id=received_message.account_assistant_id,
                        account_assistant_connection_id=received_message.account_assistant_connection_id,
                        message=received_message.message,
                        received_at=format_datetime_to_timestamp(received_message.received_at)
                    ),
                    'progress': (index / total_messages_count)
                }

    def get_account_assistant_received_messages_count(self) -> int:
        with DbSession.session_scope() as session:
            received_messages_count = session.query(self.account_assistant_received_messages_table).count()
            return received_messages_count

    def get_account_assistant_last_received_message(
            self,
            account_assistant_id: str) -> receive_account_message_pb2.AccountAssistantReceivedMessage:
        with DbSession.session_scope() as session:
            last_received_message = session.query(
                self.account_assistant_received_messages_table
            ).filter(
                self.account_assistant_received_messages_table.c.account_assistant_id == account_assistant_id
            ).order_by(
                self.account_assistant_received_messages_table.c.received_at.desc()
            ).first()
            if last_received_message is not None:
                return receive_account_message_pb2.AccountAssistantReceivedMessage(
                    account_assistant_received_message_id=last_received_message.account_assistant_received_message_id,
                    account_assistant_id=last_received_message.account_assistant_id,
                    account_assistant_connection_id=last_received_message.account_assistant_connection_id,
                    message=last_received_message.message,
                    received_at=format_datetime_to_timestamp(last_received_message.received_at)
                )
            else:
                return receive_account_message_pb2.AccountAssistantReceivedMessage()

    # TODO: Verification pending
    def get_received_messages_account_assistant_ids(self) -> [str]:
        with DbSession.session_scope() as session:
            received_messages_account_assistant_ids = []
            for distinct_received_messages_account_assistant_id in session.query(
                    self.account_assistant_received_messages_table.c.account_assistant_id
            ).distinct():
                received_messages_account_assistant_ids.append(
                    distinct_received_messages_account_assistant_id.account_assistant_id)
            return received_messages_account_assistant_ids

    # Account Sent Messages
    def get_account_sent_messages_model(self):
        class AccountSentMessages(AccountConversationModels):
            __tablename__ = self.account_sent_messages_model_name

            account_sent_message_id = Column(String(255), primary_key=True)
            account_id = Column(String(255), nullable=False)
            account_connection_id = Column(String(255), nullable=False)
            message = Column(String(), nullable=False)
            sent_at = Column(DateTime(), nullable=False)
            received_at = Column(DateTime(), nullable=True)

        return AccountSentMessages

    def get_account_sent_messages_model_name(self):
        return self.account_sent_messages_model_name

    def add_account_sent_message(self, account_id: str, account_connection_id: str,
                                 message: str, sent_at: datetime) -> str:
        account_sent_message_id = gen_uuid()
        statement = AccountConversationModels.metadata.tables[
            self.account_sent_messages_model_name].insert().values(
            account_sent_message_id=account_sent_message_id,
            account_id=account_id,
            account_connection_id=account_connection_id,
            message=message,
            sent_at=sent_at
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return account_sent_message_id

    def update_account_sent_message_received_at(self, account_sent_message_id: str,
                                                received_at: datetime):
        statement = AccountConversationModels.metadata.tables[
            self.account_sent_messages_model_name].update().values(
            received_at=received_at
        ).where(
            self.account_sent_messages_table.c.account_sent_message_id == account_sent_message_id)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def get_all_account_sent_messages(
            self
    ) -> Generator[send_account_message_pb2.AccountSentMessage, None, None]:
        with DbSession.session_scope() as session:
            all_sent_messages = session.query(self.account_sent_messages_table).all()
            for sent_message in all_sent_messages:
                if sent_message.received_at is None:
                    yield send_account_message_pb2.AccountSentMessage(
                        account_sent_message_id=sent_message.account_sent_message_id,
                        account_id=sent_message.account_id,
                        account_connection_id=sent_message.account_connection_id,
                        message=sent_message.message,
                        sent_at=format_datetime_to_timestamp(sent_message.sent_at),
                        received_at=format_datetime_to_timestamp(sent_message.received_at)
                    )

    # warn: if not received at, sending without attribute (however need to verify this later)
    def get_all_account_connected_account_sent_messages(
            self, account_id: str, filter_from_datetime: bool = False, from_datetime: datetime = None
    ) -> Generator[dict, None, None]:
        with DbSession.session_scope() as session:
            if not filter_from_datetime:
                all_account_connected_account_sent_messages = session.query(
                    self.account_sent_messages_table
                ).filter(
                    self.account_sent_messages_table.c.account_id == account_id
                ).all()
                total_count = len(all_account_connected_account_sent_messages)
            else:
                all_account_connected_account_sent_messages = session.query(
                    self.account_sent_messages_table
                ).filter(
                    self.account_sent_messages_table.c.account_id == account_id,
                    self.account_sent_messages_table.c.sent_at >= from_datetime
                ).all()
                total_count = len(all_account_connected_account_sent_messages)
            for index, sent_message in enumerate(all_account_connected_account_sent_messages):
                if sent_message.received_at is not None:
                    yield {
                        'message': send_account_message_pb2.AccountSentMessage(
                            account_sent_message_id=sent_message.account_sent_message_id,
                            account_id=sent_message.account_id,
                            account_connection_id=sent_message.account_connection_id,
                            message=sent_message.message,
                            sent_at=format_datetime_to_timestamp(sent_message.sent_at),
                            received_at=format_datetime_to_timestamp(sent_message.received_at)
                        ),
                        'progress': (index / total_count)
                    }
                else:
                    yield {
                        'message': send_account_message_pb2.AccountSentMessage(
                            account_sent_message_id=sent_message.account_sent_message_id,
                            account_id=sent_message.account_id,
                            account_connection_id=sent_message.account_connection_id,
                            message=sent_message.message,
                            sent_at=format_datetime_to_timestamp(sent_message.sent_at),
                        ),
                        'progress': (index / total_count)
                    }

    def delete_sent_message(self, account_sent_message_id):
        with DbSession.session_scope() as session:
            file = session.query(self.account_sent_messages_table).filter(
                self.account_sent_messages_table.c.account_sent_message_id == account_sent_message_id
            ).delete(synchronize_session=False)
            # session.delete(file)
            session.commit()

    def get_account_sent_messages_count(self) -> int:
        with DbSession.session_scope() as session:
            sent_messages_count = session.query(self.account_sent_messages_table).count()
            return sent_messages_count

    def get_account_last_sent_message(self, account_id: str) -> send_account_message_pb2.AccountSentMessage:
        with DbSession.session_scope() as session:
            last_sent_message = session.query(
                self.account_sent_messages_table
            ).filter(
                self.account_sent_messages_table.c.account_id == account_id
            ).order_by(
                self.account_sent_messages_table.c.sent_at.desc()
            ).first()
            if last_sent_message is not None:
                if last_sent_message.received_at is not None:
                    return send_account_message_pb2.AccountSentMessage(
                        account_sent_message_id=last_sent_message.account_sent_message_id,
                        account_id=last_sent_message.account_id,
                        account_connection_id=last_sent_message.account_connection_id,
                        message=last_sent_message.message,
                        sent_at=format_datetime_to_timestamp(last_sent_message.sent_at),
                        received_at=format_datetime_to_timestamp(last_sent_message.received_at)
                    )
                else:
                    return send_account_message_pb2.AccountSentMessage(
                        account_sent_message_id=last_sent_message.account_sent_message_id,
                        account_id=last_sent_message.account_id,
                        account_connection_id=last_sent_message.account_connection_id,
                        message=last_sent_message.message,
                        sent_at=format_datetime_to_timestamp(last_sent_message.sent_at),
                    )
            else:
                return send_account_message_pb2.AccountSentMessage()

    # TODO: Verification pending
    def get_sent_messages_account_ids(self) -> [str]:
        with DbSession.session_scope() as session:
            sent_messages_account_ids = []
            for distinct_sent_messages_account_id in session.query(
                    self.account_sent_messages_table.c.account_id
            ).distinct():
                sent_messages_account_ids.append(distinct_sent_messages_account_id.account_id)
            return sent_messages_account_ids

    # Account Received Messages
    def get_account_received_messages_model(self):
        class AccountReceivedMessages(AccountConversationModels):
            __tablename__ = self.account_received_messages_model_name

            account_received_message_id = Column(String(), primary_key=True)
            account_id = Column(String(255), nullable=False)
            account_connection_id = Column(String(255), nullable=False)
            message = Column(String())
            received_at = Column(DateTime())

        return AccountReceivedMessages

    def get_account_received_messages_model_name(self):
        return self.account_received_messages_model_name

    def add_account_received_message(self, account_received_message_id: str, account_id: str,
                                     account_connection_id: str, message: str, received_at: datetime):
        statement = AccountConversationModels.metadata.tables[
            self.account_received_messages_model_name].insert().values(
            account_received_message_id=account_received_message_id, account_id=account_id,
            account_connection_id=account_connection_id, message=message, received_at=received_at)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def get_all_account_received_messages(
            self
    ) -> Generator[receive_account_message_pb2.AccountReceivedMessage, None, None]:
        with DbSession.session_scope() as session:
            all_received_messages = session.query(self.account_received_messages_table).all()
            for received_message in all_received_messages:
                yield receive_account_message_pb2.AccountReceivedMessage(
                    account_received_message_id=received_message.account_received_message_id,
                    account_id=received_message.account_id,
                    account_connection_id=received_message.account_connection_id,
                    message=received_message.message,
                    received_at=format_datetime_to_timestamp(received_message.received_at)
                )

    def get_all_account_connected_account_received_messages(
            self, account_id: str, filter_from_datetime: bool = False, from_datetime: datetime = None
    ) -> Generator[dict, None, None]:
        with DbSession.session_scope() as session:
            if not filter_from_datetime:
                all_account_connected_account_received_messages = session.query(
                    self.account_received_messages_table
                ).filter(
                    self.account_received_messages_table.c.account_id == account_id
                ).all()
                total_messages_count = len(all_account_connected_account_received_messages)
            else:
                all_account_connected_account_received_messages = session.query(
                    self.account_received_messages_table
                ).filter(
                    self.account_received_messages_table.c.account_id == account_id,
                    self.account_received_messages_table.c.received_at >= from_datetime
                ).all()
                total_messages_count = len(all_account_connected_account_received_messages)
            for index, received_message in enumerate(all_account_connected_account_received_messages):
                yield {
                    'message': receive_account_message_pb2.AccountReceivedMessage(
                        account_received_message_id=received_message.account_received_message_id,
                        account_id=received_message.account_id,
                        account_connection_id=received_message.account_connection_id,
                        message=received_message.message,
                        received_at=format_datetime_to_timestamp(received_message.received_at)
                    ),
                    'progress': (index / total_messages_count)
                }

    def get_account_received_messages_count(self) -> int:
        with DbSession.session_scope() as session:
            received_messages_count = session.query(self.account_received_messages_table).count()
            return received_messages_count

    def get_account_last_received_message(self, account_id: str) -> receive_account_message_pb2.AccountReceivedMessage:
        with DbSession.session_scope() as session:
            last_received_message = session.query(
                self.account_received_messages_table
            ).filter(
                self.account_received_messages_table.c.account_id == account_id
            ).order_by(
                self.account_received_messages_table.c.received_at.desc()
            ).first()
            if last_received_message is not None:
                return receive_account_message_pb2.AccountReceivedMessage(
                    account_received_message_id=last_received_message.account_received_message_id,
                    account_id=last_received_message.account_id,
                    account_connection_id=last_received_message.account_connection_id,
                    message=last_received_message.message,
                    received_at=format_datetime_to_timestamp(last_received_message.received_at)
                )
            else:
                return receive_account_message_pb2.AccountReceivedMessage()

    # TODO: Verification pending
    def get_received_messages_account_ids(self) -> [str]:
        with DbSession.session_scope() as session:
            received_messages_account_ids = []
            for distinct_received_messages_account_id in session.query(
                    self.account_received_messages_table.c.account_id
            ).distinct():
                received_messages_account_ids.append(distinct_received_messages_account_id.account_id)
            print(received_messages_account_ids)
            return received_messages_account_ids
