from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    account_id = Column(String(255), primary_key=True, unique=True)
    account_personal_email_id = Column(String(255), nullable=True, unique=True)
    account_secondary_email_id = Column(String(255), nullable=True)
    account_work_email_id = Column(String(255), nullable=True, unique=True)
    account_country_code = Column(String(4), nullable=False)
    account_mobile_number = Column(String(10), nullable=True, unique=True)
    account_secondary_mobile_number = Column(String(10), nullable=True, unique=True)
    first_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=True)
    organization_id = Column(String(100), nullable=True)
    active = Column(Boolean, nullable=False)
    admin_acc = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
