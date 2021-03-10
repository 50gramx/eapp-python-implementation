import logging

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
from support.helper_functions import format_timestamp_to_datetime, get_current_timestamp

AccountAssistantConnectionModels = declarative_base()


class AccountAssistantConnections:
    def __init__(self, account_assistant_id: str):
        self.account_assistant_id = account_assistant_id
        self.account_connection_model_name = f"ac_{account_assistant_id}"
        self.account_assistant_connection_model_name = f"aac_{account_assistant_id}"
        AccountAssistantConnectionModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.account_connection_table = AccountAssistantConnectionModels.metadata.tables[
                self.account_connection_model_name]
            self.account_assistant_connection_table = AccountAssistantConnectionModels.metadata.tables[
                self.account_assistant_connection_model_name]
        except KeyError:
            self.account_connection_table = None
            self.account_assistant_connection_table = None

    # Setup Account Assistant Connection
    def setup_account_assistant_connections(self):
        self.get_account_connection_model().__table__.create(bind=DbSession.get_engine())
        self.get_account_assistant_connection_model().__table__.create(bind=DbSession.get_engine())
        logging.info(f'account assistant connections setup successfully for account id: {self.account_assistant_id}')
        return

    # Account Connection
    def get_account_connection_model(self):
        class AccountConnection(AccountAssistantConnectionModels):
            __tablename__ = self.account_connection_model_name

            account_connection_id = Column(String(255), primary_key=True, unique=True)
            account_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime, nullable=False)

        return AccountConnection

    def get_account_connection_model_name(self):
        return self.account_connection_model_name

    def add_new_account_connection(self, account_connection_id: str, account_id: str):
        statement = AccountAssistantConnectionModels.metadata.tables[
            self.account_connection_model_name].insert().values(
            account_connection_id=account_connection_id,
            account_id=account_id,
            connected_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return

    def is_account_connected(self, account_connection_id: str, account_id: str) -> bool:
        with DbSession.session_scope() as session:
            statement = session.query(self.account_assistant_connection_table).filter(
                self.account_connection_table.c.account_connection_id == account_connection_id,
                self.account_connection_table.c.account_id == account_id
            )
            account_connected = session.query(statement.exists()).scalar()
            return account_connected

    # Account Assistant Connection
    def get_account_assistant_connection_model(self):
        class AccountAssistantConnection(AccountAssistantConnectionModels):
            __tablename__ = self.account_assistant_connection_model_name

            account_assistant_connection_id = Column(String(255), primary_key=True, unique=True)
            account_assistant_id = Column(String(255), nullable=False)
            connected_at = Column(DateTime(), nullable=False)

        return AccountAssistantConnection

    def get_account_assistant_connection_model_name(self):
        return self.account_assistant_connection_model_name
