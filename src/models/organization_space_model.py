from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OrgSpace(Base):
    __tablename__ = 'org_space'

    space_id = Column(String, primary_key=True)
    space_name = Column(String, nullable=False, unique=True)
    white_knowledge_domain_id = Column(String, ForeignKey("knowledge_domain.knowledge_domain_id"), nullable=False)
    white_knowledge_domain_name = Column(String, nullable=False)
    organization_id = Column(String, ForeignKey("organization.organization_id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
