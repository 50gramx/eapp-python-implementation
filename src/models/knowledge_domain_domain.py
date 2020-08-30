from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KnowledgeDomain(Base):
    __tablename__ = 'knowledge_domain'

    knowledge_domain_id = Column(String, primary_key=True, unique=True)
    knowledge_domain_name = Column(String, nullable=False)
    knowledge_domain_description = Column(String)
    knowledge_domain_color = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)
