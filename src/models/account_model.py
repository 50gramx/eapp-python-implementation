from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'

    account_id = Column(String, primary_key=True, unique=True)
    account_email_id = Column(String, nullable=False, unique=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    organization_id = Column(String, ForeignKey("organization.organization_id"), nullable=False)
    active = Column(Boolean, nullable=False)
    admin_acc = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
