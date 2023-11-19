from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
from support.helper_functions import gen_uuid

AccountAssistantConversationModels = declarative_base()


# ----------------------------------------
# Account Assistant Conversation Models
# ----------------------------------------
class AccountAssistantConversations:
    def __init__(self, account_assistant_id: str):
        self.account_assistant_id = account_assistant_id
        self.account_sent_messages_model_name = f"aacasm_{account_assistant_id}"
        self.account_received_messages_model_name = f"aacarm_{account_assistant_id}"
        AccountAssistantConversationModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.account_sent_messages_table = AccountAssistantConversationModels.metadata.tables[
                self.account_sent_messages_model_name]
            self.account_received_messages_table = AccountAssistantConversationModels.metadata.tables[
                self.account_received_messages_model_name]
        except KeyError:
            self.account_sent_messages_table = None
            self.account_received_messages_table = None

    # Setup Account Conversations
    def setup_account_conversations(self):
        self.get_account_sent_messages_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_received_messages_model().__table__.create(bind=DbSession.get_engine())
        return

    # ----------------------------------------
    # Account Sent Messages
    # ----------------------------------------
    def get_account_sent_messages_model(self):
        class AccountSentMessages(AccountAssistantConversationModels):
            __tablename__ = self.account_sent_messages_model_name

            account_sent_message_id = Column(String(), primary_key=True)
            account_id = Column(String(255), nullable=False)
            account_connection_id = Column(String(255), nullable=False)
            message = Column(String())
            message_source_space_id = Column(String(255))
            message_source_space_type_id = Column(String(255))
            message_source_space_domain_id = Column(String(255))
            message_source_space_domain_action = Column(Integer)
            message_source_space_domain_action_context_id = Column(String(255))
            sent_at = Column(DateTime())
            received_at = Column(DateTime())

        return AccountSentMessages

    def get_account_sent_messages_model_name(self):
        return self.account_sent_messages_model_name

    def add_account_sent_message(self, account_id: str, account_connection_id: str, message: str,
                                 message_source_space_id: str, message_source_space_type_id: str,
                                 message_source_space_domain_id: str, message_source_space_domain_action: int,
                                 message_source_space_domain_action_context_id: str,
                                 sent_at: datetime) -> str:
        account_sent_message_id = gen_uuid()
        statement = AccountAssistantConversationModels.metadata.tables[
            self.account_sent_messages_model_name].insert().values(
            account_sent_message_id=account_sent_message_id,
            account_id=account_id,
            account_connection_id=account_connection_id,
            message=message,
            message_source_space_id=message_source_space_id,
            message_source_space_domain_id=message_source_space_domain_id,
            message_source_space_domain_action=message_source_space_domain_action,
            message_source_space_domain_action_context_id=message_source_space_domain_action_context_id,
            sent_at=sent_at
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return account_sent_message_id

    def update_account_sent_message_received_at(self, account_sent_message_id: str,
                                                received_at: datetime):
        statement = AccountAssistantConversationModels.metadata.tables[
            self.account_sent_messages_model_name].update().values(
            received_at=received_at
        ).where(
            self.account_sent_messages_table.c.account_sent_message_id == account_sent_message_id)
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    # ----------------------------------------
    # Account Received Messages
    # ----------------------------------------
    def get_account_received_messages_model(self):
        class AccountReceivedMessages(AccountAssistantConversationModels):
            __tablename__ = self.account_received_messages_model_name

            account_received_message_id = Column(String(), primary_key=True)
            account_id = Column(String(255), nullable=False)
            account_connection_id = Column(String(255), nullable=False)
            message = Column(String(), nullable=False)
            message_space = Column(Integer, nullable=False)
            message_space_action = Column(Integer, nullable=False)
            received_at = Column(DateTime(), nullable=False)

        return AccountReceivedMessages

    def get_account_received_messages_model_name(self):
        return self.account_received_messages_model_name

    def add_account_received_message(self, account_received_message_id: str, account_id: str,
                                     account_connection_id: str,
                                     message: str, message_space: int, message_space_action: int,
                                     received_at: datetime):
        statement = AccountAssistantConversationModels.metadata.tables[
            self.account_received_messages_model_name].insert().values(
            account_received_message_id=account_received_message_id,
            account_id=account_id,
            account_connection_id=account_connection_id,
            message=message,
            message_space=message_space,
            message_space_action=message_space_action,
            received_at=received_at
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return
