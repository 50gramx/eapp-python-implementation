from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organization'

    organization_id = Column(String, primary_key=True, unique=True)
    organization_name = Column(String, nullable=False)
    organization_space_id = Column(String, ForeignKey("org_space.space_id"), nullable=False, unique=True)
    organization_admin_acc_id = Column(String, ForeignKey("account.account_id"), nullable=False)
    active = Column(Boolean, nullable=False)
    billing_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)