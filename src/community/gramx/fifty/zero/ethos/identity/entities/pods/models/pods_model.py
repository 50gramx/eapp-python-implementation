from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from db_session import DbSession
from support.helper_functions import gen_uuid, format_timestamp_to_datetime, get_current_timestamp

DynamicPodsModels = declarative_base()

class Pod:
    def __init__(self, pod_id: str):
        self.pod_id = pod_id
        self.container_table_name = f"containers_{pod_id}"
        self.env_var_table_name = f"env_vars_{pod_id}"
        self.ssh_credentials_table_name = f"ssh_credentials_{pod_id}"
        DynamicPodsModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.container_table = DynamicPodsModels.metadata.tables[self.container_table_name]
            self.env_var_table = DynamicPodsModels.metadata.tables[self.env_var_table_name]
            self.ssh_credentials_table = DynamicPodsModels.metadata.tables[self.ssh_credentials_table_name]
        except KeyError:
            self.container_table = None
            self.env_var_table = None
            self.ssh_credentials_table = None

    def setup_pod(self):
        """Create all related tables dynamically based on the pod ID."""
        self.get_container_model().__table__.create(bind=DbSession.get_engine())
        self.get_env_var_model().__table__.create(bind=DbSession.get_engine())
        self.get_ssh_credentials_model().__table__.create(bind=DbSession.get_engine())
        return

    # Container Model for Pod
    def get_container_model(self):
        class Containers(DynamicPodsModels):
            __tablename__ = self.container_table_name

            container_id = Column(String(255), primary_key=True, unique=True)
            container_name = Column(String(255), nullable=False)
            container_image = Column(String(255), nullable=False)
            container_ports = Column(Integer, nullable=False)
            pod_id = Column(String(255), ForeignKey('pods.pod_id'), nullable=False)
            created_at = Column(DateTime, nullable=False)

        return Containers

    # Environment Variables Model for Pod
    def get_env_var_model(self):
        class EnvVars(DynamicPodsModels):
            __tablename__ = self.env_var_table_name

            env_var_id = Column(String(255), primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            value = Column(String(255), nullable=False)
            container_id = Column(String(255), ForeignKey(f"{self.container_table_name}.container_id"), nullable=False)

        return EnvVars

    # SSH Credentials Model for Pod
    def get_ssh_credentials_model(self):
        class SSHPodCredentials(DynamicPodsModels):
            __tablename__ = self.ssh_credentials_table_name

            ssh_credential_id = Column(String(255), primary_key=True, unique=True)
            user_name = Column(String(255), nullable=False)
            node_ip = Column(String(255), nullable=False)
            ssh_command = Column(String(255), nullable=False)
            last_login = Column(DateTime, nullable=False)
            pod_id = Column(String(255), ForeignKey('pods.pod_id'), nullable=False)

        return SSHPodCredentials

    # Methods to add, retrieve and manage the pod entities dynamically
    def add_container(self, container_name: str, container_image: str, container_ports: int):
        container_id = gen_uuid()
        statement = DynamicPodsModels.metadata.tables[self.container_table_name].insert().values(
            container_id=container_id,
            container_name=container_name,
            container_image=container_image,
            container_ports=container_ports,
            pod_id=self.pod_id,
            created_at=format_timestamp_to_datetime(get_current_timestamp()),
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return container_id

    def get_all_containers(self):
        with DbSession.session_scope() as session:
            containers = session.query(self.container_table).all()
            return containers

    def add_env_var(self, container_id: str, name: str, value: str):
        env_var_id = gen_uuid()
        statement = DynamicPodsModels.metadata.tables[self.env_var_table_name].insert().values(
            env_var_id=env_var_id,
            name=name,
            value=value,
            container_id=container_id
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return env_var_id

    def get_all_env_vars(self):
        with DbSession.session_scope() as session:
            env_vars = session.query(self.env_var_table).all()
            return env_vars

    def add_ssh_credentials(self, user_name: str, node_ip: str, ssh_command: str):
        ssh_credential_id = gen_uuid()
        statement = DynamicPodsModels.metadata.tables[self.ssh_credentials_table_name].insert().values(
            ssh_credential_id=ssh_credential_id,
            user_name=user_name,
            node_ip=node_ip,
            ssh_command=ssh_command,
            last_login=format_timestamp_to_datetime(get_current_timestamp()),
            pod_id=self.pod_id
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return ssh_credential_id

    def get_ssh_credentials(self):
        with DbSession.session_scope() as session:
            credentials = session.query(self.ssh_credentials_table).all()
            return credentials
