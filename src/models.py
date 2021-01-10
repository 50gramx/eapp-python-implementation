from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    account_analytics_id = Column(String(255), primary_key=True, unique=True)
    account_id = Column(String(255), primary_key=True, unique=True)
    account_personal_email_id = Column(String(255), nullable=True, unique=True)
    account_work_email_id = Column(String(255), nullable=True, unique=True)
    account_country_code = Column(String(6), nullable=False)
    account_mobile_number = Column(String(10), nullable=False, unique=True)
    account_first_name = Column(String(40), nullable=False)
    account_last_name = Column(String(40), nullable=False)
    account_gender = Column(String(10), nullable=False)
    account_born_at = Column(DateTime(), nullable=False)
    account_created_at = Column(DateTime(), nullable=False)


class AccountSecrets(Base):
    __tablename__ = 'account_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_password = Column(String(255), nullable=False)
    account_password_last_updated_geo_lat = Column(String(255), nullable=False)
    account_password_last_updated_geo_long = Column(String(255), nullable=False)
    account_password_last_updated_at = Column(DateTime())
    account_password_created_at = Column(DateTime(), nullable=False)


class AccountConvenienceSecrets(Base):
    __tablename__ = 'account_convenience_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_convenience_pin = Column(String(6), nullable=False)
    account_convenience_pin_created_at = Column(DateTime(), nullable=False)
