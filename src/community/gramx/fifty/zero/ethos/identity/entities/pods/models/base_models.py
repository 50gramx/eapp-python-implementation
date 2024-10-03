from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseModels = declarative_base()

# Base model for Pods
class Pods(BaseModels):
    __tablename__ = 'pods'

    pod_id = Column(String(255), primary_key=True, unique=True)
    pod_name = Column(String(255), nullable=False)
    pod_image = Column(String(255), nullable=False)
    expiration_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)


# Base model for Containers in each Pod
class PodContainers(BaseModels):
    __tablename__ = 'pod_containers'

    container_id = Column(String(255), primary_key=True, unique=True)
    container_name = Column(String(255), nullable=False)
    container_image = Column(String(255), nullable=False)
    pod_id = Column(String(255), ForeignKey('pods.pod_id'), nullable=False)
    created_at = Column(DateTime, nullable=False)


# Base model for Node Information
class NodeInfo(BaseModels):
    __tablename__ = 'node_info'

    node_name = Column(String(255), primary_key=True, unique=True)
    status = Column(String(255), nullable=False)
    pod_id = Column(String(255), ForeignKey('pods.pod_id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
