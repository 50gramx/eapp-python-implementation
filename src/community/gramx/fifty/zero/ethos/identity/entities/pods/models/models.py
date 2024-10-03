from sqlalchemy import (
    Column, String, Integer, ForeignKey, Table,
    Map, DateTime, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EnvVar(Base):
    __tablename__ = 'env_vars'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

class Pod(Base):
    __tablename__ = 'pods'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=False)
    expiration_time = Column(DateTime)

    # Relationships
    env_vars = relationship('EnvVar', secondary='pod_env_vars', back_populates='pods')
    containers = relationship('Container', back_populates='pod')

class Container(Base):
    __tablename__ = 'containers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    pod_id = Column(Integer, ForeignKey('pods.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    env_vars = relationship('EnvVar', secondary='container_env_vars', back_populates='containers')
    pod = relationship('Pod', back_populates='containers')

class SSHPodCredentials(Base):
    __tablename__ = 'ssh_pod_credentials'
    
    id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    node_ip = Column(String, nullable=False)
    ssh_command = Column(String, nullable=False)
    last_login = Column(DateTime)

class NodeInfo(Base):
    __tablename__ = 'nodes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    addresses = Column(JSON, nullable=False)  # Stores a map of addresses
    labels = Column(JSON, nullable=False)      # Stores a map of labels
    annotations = Column(JSON, nullable=False)  # Stores a map of annotations
    status = Column(String, nullable=False)

# Association Tables
pod_env_vars = Table(
    'pod_env_vars', Base.metadata,
    Column('pod_id', Integer, ForeignKey('pods.id')),
    Column('env_var_id', Integer, ForeignKey('env_vars.id'))
)

container_env_vars = Table(
    'container_env_vars', Base.metadata,
    Column('container_id', Integer, ForeignKey('containers.id')),
    Column('env_var_id', Integer, ForeignKey('env_vars.id'))
)
