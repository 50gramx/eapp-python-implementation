#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import logging

import ethos.elint.collars.DC499999999_pb2 as cpb2
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db_session import DbSession
from src.community.gramx.fifty.zero.ethos.service_spaces.models.base import (
    ServiceSpaceModelBase,
)
from src.support.helper_functions import (
    format_datetime_to_timestamp,
    format_timestamp_to_datetime,
    gen_uuid,
    get_current_timestamp,
)

# TODO(Anyone): Add README.md + Code Documentations & Comments


class DC499999999Model:
    def __init__(
        self,
        space_service_domain_id: str,
        space_service_domain_collar_code: str,
    ):
        self.domain_id = space_service_domain_id
        self.domain_collar_code = space_service_domain_collar_code

        self.deployment_model_name = self._get_table_name(code=5000)
        self.selector_model_name = self._get_table_name(code=5001)
        self.pod_template_model_name = self._get_table_name(code=5002)
        self.metadata_model_name = self._get_table_name(code=5008)
        self.replica_config_model_name = self._get_table_name(code=5009)
        self.networking_config_model_name = self._get_table_name(code=5011)
        self.metadata_labels_model_name = self._get_table_name(code=5012)
        self.metadata_annotations_model_name = self._get_table_name(code=5013)
        self.selector_labels_model_name = self._get_table_name(code=5014)
        self.selector_expressions_model_name = self._get_table_name(code=5015)
        self.template_labels_model_name = self._get_table_name(code=5016)
        self.template_annotations_model_name = self._get_table_name(code=5017)
        self.template_containers_model_name = self._get_table_name(code=5018)
        self.template_volumes_model_name = self._get_table_name(code=5019)
        self.container_command_model_name = self._get_table_name(code=5020)
        self.container_args_model_name = self._get_table_name(code=5021)
        self.container_ports_model_name = self._get_table_name(code=5022)
        self.container_envs_model_name = self._get_table_name(code=5023)
        self.container_requests_model_name = self._get_table_name(code=5024)
        self.container_limits_model_name = self._get_table_name(code=5025)
        # self.container_mounts_model_name = self._get_table_name(code=5026)
        self.collar_model_name = self._get_table_name(code=9999)
        try:
            self.collar_table = ServiceSpaceModelBase.metadata.tables[
                self.collar_model_name
            ]
            self.deployment_table = ServiceSpaceModelBase.metadata.tables[
                self.deployment_model_name
            ]
            self.metadata_table = ServiceSpaceModelBase.metadata.tables[
                self.metadata_model_name
            ]
            self.metadata_labels_table = ServiceSpaceModelBase.metadata.tables[
                self.metadata_labels_model_name
            ]
            self.metadata_annotations_table = ServiceSpaceModelBase.metadata.tables[
                self.metadata_annotations_model_name
            ]
            self.replica_config_table = ServiceSpaceModelBase.metadata.tables[
                self.replica_config_model_name
            ]
            self.networking_config_table = ServiceSpaceModelBase.metadata.tables[
                self.networking_config_model_name
            ]
            self.selector_table = ServiceSpaceModelBase.metadata.tables[
                self.selector_model_name
            ]
            self.selector_labels_table = ServiceSpaceModelBase.metadata.tables[
                self.selector_labels_model_name
            ]
            self.selector_expressions_table = ServiceSpaceModelBase.metadata.tables[
                self.selector_expressions_model_name
            ]
            self.pod_template_table = ServiceSpaceModelBase.metadata.tables[
                self.pod_template_model_name
            ]
            self.template_labels_table = ServiceSpaceModelBase.metadata.tables[
                self.template_labels_model_name
            ]
            self.template_annotations_table = ServiceSpaceModelBase.metadata.tables[
                self.template_annotations_model_name
            ]
            self.template_containers_table = ServiceSpaceModelBase.metadata.tables[
                self.template_containers_model_name
            ]
            self.template_volumes_table = ServiceSpaceModelBase.metadata.tables[
                self.template_volumes_model_name
            ]
            self.container_command_table = ServiceSpaceModelBase.metadata.tables[
                self.container_command_model_name
            ]
            self.container_args_table = ServiceSpaceModelBase.metadata.tables[
                self.container_args_model_name
            ]
            self.container_ports_table = ServiceSpaceModelBase.metadata.tables[
                self.container_ports_model_name
            ]
            self.container_envs_table = ServiceSpaceModelBase.metadata.tables[
                self.container_envs_model_name
            ]
            self.container_requests_table = ServiceSpaceModelBase.metadata.tables[
                self.container_requests_model_name
            ]
            self.container_limits_table = ServiceSpaceModelBase.metadata.tables[
                self.container_limits_model_name
            ]
            # self.container_mounts_table = ServiceSpaceModelBase.metadata.tables[
            #     self.container_mounts_model_name
            # ]
        except Exception as e:
            logging.info(f"DC499999999Model: init, KeyError: {e}")
            self.collar_table = None
            self.deployment_table = None
            self.metadata_table = None
            self.metadata_labels_table = None
            self.metadata_annotations_table = None
            self.replica_config_table = None
            self.networking_config_table = None
            self.selector_table = None
            self.selector_labels_table = None
            self.selector_expressions_table = None
            self.pod_template_table = None
            self.template_labels_table = None
            self.template_annotations_table = None
            self.template_containers_table = None
            self.template_volumes_table = None
            self.container_command_table = None
            self.container_args_table = None
            self.container_ports_table = None
            self.container_envs_table = None
            self.container_requests_table = None
            self.container_limits_table = None
            # self.container_mounts_table = None

    def _get_table_name(self, code: int) -> str:
        return f"{self.domain_collar_code}_{code}_{self.domain_id}"

    # Setup Domain Service Space
    def setup_domain_collar_service_space(self):
        self.get_deployment_model().__table__.create(bind=DbSession.get_engine())
        # Deployment Entities
        self.get_pod_template_model().__table__.create(bind=DbSession.get_engine())
        self.get_selector_model().__table__.create(bind=DbSession.get_engine())
        self.get_metadata_model().__table__.create(bind=DbSession.get_engine())
        self.get_networking_config_model().__table__.create(bind=DbSession.get_engine())
        self.get_replica_config_model().__table__.create(bind=DbSession.get_engine())

        # Deployment Metadata Entities
        self.get_metadata_labels_model().__table__.create(bind=DbSession.get_engine())
        self.get_metadata_annotations_model().__table__.create(
            bind=DbSession.get_engine()
        )

        # Deployment Label Selector Entities
        self.get_selector_expressions_model().__table__.create(
            bind=DbSession.get_engine()
        )
        self.get_selector_labels_model().__table__.create(bind=DbSession.get_engine())

        # Pod Template Entities
        self.get_template_volumes_model().__table__.create(bind=DbSession.get_engine())
        self.get_template_containers_model().__table__.create(
            bind=DbSession.get_engine()
        )
        self.get_template_annotations_model().__table__.create(
            bind=DbSession.get_engine()
        )
        self.get_template_labels_model().__table__.create(bind=DbSession.get_engine())

        # Container Entities
        self.get_container_command_model().__table__.create(bind=DbSession.get_engine())
        self.get_container_args_model().__table__.create(bind=DbSession.get_engine())
        self.get_container_ports_model().__table__.create(bind=DbSession.get_engine())
        self.get_container_envs_model().__table__.create(bind=DbSession.get_engine())
        self.get_container_requests_model().__table__.create(
            bind=DbSession.get_engine()
        )
        self.get_container_limits_model().__table__.create(bind=DbSession.get_engine())
        # self.get_container_mounts_model().__table__.create(bind=DbSession.get_engine())

        # Collar Entities

        self.get_DC499999999_collar_model().__table__.create(
            bind=DbSession.get_engine()
        )
        return

    def get_DC499999999_collar_model(self):
        class DC499999999(ServiceSpaceModelBase):
            __tablename__ = self.collar_model_name

            id = Column(String, primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            description = Column(String)

            # One-to-One relationship with Deployment
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            deployment = relationship(
                "Deployment", back_populates=f"{self.collar_model_name}", uselist=False
            )

            created_at = Column(DateTime(), nullable=False)
            updated_at = Column(DateTime(), nullable=False)

        return DC499999999

    def get_collar(self, id) -> cpb2.DC499999999:
        with DbSession.session_scope() as session:
            collar = (
                session.query(self.collar_table)
                .filter(self.collar_table.c.id == id)
                .first()
            )
            return cpb2.DC499999999(
                id=collar.id,
                name=collar.name,
                description=collar.description,
                deployment=self.get_deployment_proto(collar.deployment_id),
                created_at=format_datetime_to_timestamp(collar.created_at),
                updated_at=format_datetime_to_timestamp(collar.created_at),
            )

    def get_collar_proto_latest(self) -> cpb2.DC499999999:
        with DbSession.session_scope() as session:
            logging.info(f"get_collar_proto_latest: {type(self.collar_table)}")
            collar = (
                session.query(self.collar_table)
                .order_by(self.collar_table.c.updated_at.desc())
                .first()
            )
            if collar is None:
                return cpb2.DC499999999()
            return self.get_collar(collar.id)

    def get_collar_all(self) -> list:
        with DbSession.session_scope() as session:
            collars = session.query(self.collar_table).all()
            return [
                cpb2.DC499999999(
                    id=collar.id,
                    name=collar.name,
                    description=collar.description,
                    deployment=self.get_deployment_proto(collar.deployment_id),
                    created_at=format_datetime_to_timestamp(collar.created_at),
                    updated_at=format_datetime_to_timestamp(collar.created_at),
                )
                for collar in collars
            ]

    def add_collar(
        self, deployment_id: str, name: str = "", description: str = ""
    ) -> str:
        """Add deployment data from a protobuf object into the database."""

        # reserve new id
        id = gen_uuid()

        # add collar record statement
        statement = (
            ServiceSpaceModelBase.metadata.tables[self.collar_model_name]
            .insert()
            .values(
                id=id,
                name=name,
                description=description,
                deployment_id=deployment_id,
                created_at=format_timestamp_to_datetime(get_current_timestamp()),
                updated_at=format_timestamp_to_datetime(get_current_timestamp()),
            )
        )

        # Commit to save all changes
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

        # Pass collar id
        return id

    def get_deployment_model(self):
        class Deployment(ServiceSpaceModelBase):
            __tablename__ = self.deployment_model_name

            id = Column(String, primary_key=True)

            # TODO: fix unused params
            # One-to-One Relationships
            deployment_metadata = relationship(
                "DeploymentMetadata",
                uselist=False,
                back_populates=self.deployment_model_name,
            )  # Used
            replica_config = relationship(
                "ReplicaConfig",
                uselist=False,
                back_populates=self.deployment_model_name,
            )  # Used
            # rollout_settings = relationship(
            #     "RolloutSettings",
            #     uselist=False,
            #     back_populates=self.deployment_model_name,
            # )  # Not Used
            networking_config = relationship(
                "NetworkingConfig",
                uselist=False,
                back_populates=self.deployment_model_name,
            )  # Partially Used

            # One-to-Many Relationships (Collar Entities)
            selector = relationship(
                "LabelSelector", uselist=True, back_populates=self.deployment_model_name
            )  # Used
            pod_template = relationship(
                "PodTemplate", uselist=True, back_populates=self.deployment_model_name
            )  # Used
            # affinity_rules = relationship(
            #     "AffinityRule", back_populates=self.deployment_model_name
            # )  # Not Used
            # node_selector = relationship(
            #     "NodeSelector", uselist=True, back_populates=self.deployment_model_name
            # )  # Not Used
            # tolerations = relationship(
            #     "Toleration", back_populates=self.deployment_model_name
            # )  # Not Used
            # lifecycle_hooks = relationship(
            #     "LifecycleHook", uselist=True, back_populates=self.deployment_model_name
            # )  # Not Used
            # priority_class = relationship(
            #     "PriorityClass", uselist=True, back_populates=self.deployment_model_name
            # )  # Not Used

        return Deployment

    def add_deployment_from_proto(self, deployment_proto: cpb2.Deployment) -> str:
        """Add deployment data from a protobuf object into the database."""

        # reserve new id
        id = gen_uuid()

        # add deployment record statement
        statement = (
            ServiceSpaceModelBase.metadata.tables[self.deployment_model_name]
            .insert()
            .values(
                id=id,
            )
        )

        # Commit to save all changes
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()

        # Add related entities like metadata, labels, and annotations
        # TODO: for rest params
        if deployment_proto.HasField("metadata"):
            self._add_metadata_from_proto(deployment_proto.metadata, id)
        if deployment_proto.HasField("replica_config"):
            self._add_replica_config_from_proto(deployment_proto.replica_config, id)
        if deployment_proto.HasField("replica_config"):
            self._add_network_config_from_proto(deployment_proto.networking_config, id)
        if deployment_proto.HasField("selector"):
            self._add_selector_from_proto(deployment_proto.selector, id)
        if deployment_proto.HasField("pod_template"):
            self._add_pod_template_from_proto(deployment_proto.pod_template, id)

        # Pass deployment id
        return id

    def get_deployment_proto(self, deployment_id) -> cpb2.Deployment:
        with DbSession.session_scope() as session:
            # Fetch deployment record from the database
            deployment = (
                session.query(self.deployment_table)
                .filter(self.deployment_table.c.id == deployment_id)
                .first()
            )
            if not deployment:
                raise ValueError(f"Deployment with ID {deployment_id} not found")

            # Fetch related pod template, replica config, etc., if needed
            deployment_metadata = (
                session.query(self.metadata_table)
                .filter(self.metadata_table.c.deployment_id == deployment_id)
                .first()
            )
            pod_template = (
                session.query(self.pod_template_table)
                .filter(self.pod_template_table.c.deployment_id == deployment_id)
                .first()
            )
            replica_config = (
                session.query(self.replica_config_table)
                .filter(self.replica_config_table.c.deployment_id == deployment_id)
                .first()
            )

            # Handle missing pod template or replica config
            if not deployment_metadata:
                logging.warning("not deployment_metadata")
                deployment_metadata = cpb2.DeploymentMetadata()
            if not pod_template:
                pod_template = cpb2.PodTemplate()
                logging.warning("not pod_template")
            if not replica_config:
                replica_config = cpb2.ReplicaConfig()
                logging.warning("not replica_config")

            metadata_proto = cpb2.DeploymentMetadata(
                id=f"{deployment_metadata.id}",
                deployment_id=deployment_id,
                name=getattr(
                    deployment_metadata, "name", "default-name"
                ),  # Fallback to default
                namespace=getattr(
                    deployment_metadata, "namespace", "default-namespace"
                ),
                labels=self.get_metadata_labels(deployment_metadata.id),
                annotations=dict(getattr(deployment_metadata, "annotations", {})),
            )

            # Construct the Deployment proto
            deployment_proto = cpb2.Deployment(
                id=deployment_id,
                metadata=metadata_proto,
                replica_config=cpb2.ReplicaConfig(
                    id=f"{replica_config.id}",
                    deployment_id=deployment_id,
                    replicas=getattr(replica_config, "replicas", 1),
                    strategy=getattr(replica_config, "strategy", "RollingUpdate"),
                    min_ready_seconds=getattr(replica_config, "min_ready_seconds", 0),
                ),
                pod_template=cpb2.PodTemplate(
                    id=f"{pod_template.id}",
                    deployment_id=deployment_id,
                    labels=dict(
                        getattr(pod_template, "labels", {})
                    ),  # Safely fetch or use default
                    annotations=dict(getattr(pod_template, "annotations", {})),
                    containers=self.get_containers_proto(pod_template.id),
                ),
                # selector=cpb2.LabelSelector(
                #     match_labels=dict(deployment.selector_match_labels or {}),
                # ),
                # createdAt=format_datetime_to_timestamp(deployment.created_at),
                # updatedAt=format_datetime_to_timestamp(deployment.updated_at),
            )

            return deployment_proto

    def get_metadata_model(self):
        class DeploymentMetadata(ServiceSpaceModelBase):
            __tablename__ = self.metadata_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            name = Column(String, nullable=False)
            namespace = Column(String, nullable=False)

            # These fields will be represented by separate label and annotation tables
            labels = relationship(
                "MetadataLabels", back_populates=self.metadata_model_name
            )
            annotations = relationship(
                "MetadataAnnotations", back_populates=self.metadata_model_name
            )

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "Deployment", back_populates=self.metadata_model_name
            )

        return DeploymentMetadata

    def _add_metadata_from_proto(
        self, metadata_proto: cpb2.DeploymentMetadata, deployment_id: str
    ):
        """Add metadata and its labels/annotations from protobuf into the database."""
        # Populate deployment metadata
        with DbSession.session_scope() as session:
            metadata_statement = (
                ServiceSpaceModelBase.metadata.tables[self.metadata_model_name]
                .insert()
                .values(
                    deployment_id=deployment_id,
                    name=metadata_proto.name,
                    namespace=metadata_proto.namespace,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[self.metadata_model_name].c.id
                )
            )
            result = session.execute(metadata_statement)
            metadata_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        # Add labels
        with DbSession.session_scope() as session:
            for k, v in metadata_proto.labels.items():
                label_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.metadata_labels_model_name
                    ]
                    .insert()
                    .values(
                        metadata_id=metadata_id,
                        key=k,
                        value=v,
                    )
                )
                session.execute(label_statement)
            session.commit()

        # Add annotations
        with DbSession.session_scope() as session:
            for k, v in metadata_proto.annotations.items():
                annotation_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.metadata_annotations_model_name
                    ]
                    .insert()
                    .values(
                        metadata_id=metadata_id,
                        key=k,
                        value=v,
                    )
                )
                session.execute(annotation_statement)
            session.commit()

        return metadata_id

    def get_metadata_labels(self, metadata_id: str) -> dict:
        with DbSession.session_scope() as session:
            # Fetch existing labels for the given metadata ID
            existing_labels = (
                session.query(
                    self.metadata_labels_table.c.key, self.metadata_labels_table.c.value
                )
                .filter(self.metadata_labels_table.c.metadata_id == metadata_id)
                .all()
            )

            # Convert existing labels to a dictionary
            existing_labels_dict = {key: value for key, value in existing_labels}
            return existing_labels_dict

    def update_metadata_labels_from_proto(
        self, metadata_proto: cpb2.DeploymentMetadata
    ):
        # Add labels
        with DbSession.session_scope() as session:
            # Fetch existing labels for the given metadata ID
            existing_labels = (
                session.query(
                    self.metadata_labels_table.c.key, self.metadata_labels_table.c.value
                )
                .filter(self.metadata_labels_table.c.metadata_id == metadata_proto.id)
                .all()
            )

            # Convert existing labels to a dictionary
            existing_labels_dict = {key: value for key, value in existing_labels}

            # Determine keys to update, insert, and delete
            new_labels = metadata_proto.labels
            keys_to_update = {
                k: v
                for k, v in new_labels.items()
                if k in existing_labels_dict and existing_labels_dict[k] != v
            }
            keys_to_insert = {
                k: v for k, v in new_labels.items() if k not in existing_labels_dict
            }
            keys_to_delete = {
                k for k in existing_labels_dict.keys() if k not in new_labels
            }

            # Update existing keys with new values
            for k, v in keys_to_update.items():
                update_statement = (
                    self.metadata_labels_table.update()
                    .where(
                        (self.metadata_labels_table.c.metadata_id == metadata_proto.id)
                        & (self.metadata_labels_table.c.key == k)
                    )
                    .values(value=v)
                )
                session.execute(update_statement)

            # Insert new keys
            for k, v in keys_to_insert.items():
                insert_statement = self.metadata_labels_table.insert().values(
                    metadata_id=metadata_proto.id, key=k, value=v
                )
                session.execute(insert_statement)

            # Delete missing keys
            for k in keys_to_delete:
                delete_statement = self.metadata_labels_table.delete().where(
                    (self.metadata_labels_table.c.metadata_id == metadata_proto.id)
                    & (self.metadata_labels_table.c.key == k)
                )
                session.execute(delete_statement)

            # Commit the transaction
            session.commit()
        pass

    def get_metadata_labels_model(self):
        class MetadataLabels(ServiceSpaceModelBase):
            __tablename__ = self.metadata_labels_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            metadata_id = Column(Integer, ForeignKey(f"{self.metadata_model_name}.id"))
            key = Column(String, nullable=False)
            value = Column(String, nullable=False)

            deployment_metadata = relationship(
                "DeploymentMetadata", back_populates=self.metadata_labels_model_name
            )

        return MetadataLabels

    def get_metadata_annotations_model(self):
        class MetadataAnnotations(ServiceSpaceModelBase):
            __tablename__ = self.metadata_annotations_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            metadata_id = Column(Integer, ForeignKey(f"{self.metadata_model_name}.id"))
            key = Column(String, nullable=False)
            value = Column(String, nullable=False)

            deployment_metadata = relationship(
                "DeploymentMetadata",
                back_populates=self.metadata_annotations_model_name,
            )

        return MetadataAnnotations

    def get_replica_config_model(self):
        class ReplicaConfig(ServiceSpaceModelBase):
            __tablename__ = self.replica_config_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            replicas = Column(Integer, nullable=False)  # Number of replicas
            strategy = Column(
                String, nullable=False
            )  # Deployment strategy (e.g., RollingUpdate, Recreate)
            min_ready_seconds = Column(Integer, nullable=False)  # Minimum ready seconds

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "Deployment", back_populates=self.replica_config_model_name
            )

        return ReplicaConfig

    def _add_replica_config_from_proto(
        self, rc: cpb2.ReplicaConfig, deployment_id: str
    ):
        """Add metadata and its labels/annotations from protobuf into the database."""
        # Populate deployment metadata
        with DbSession.session_scope() as session:
            rc_statement = (
                ServiceSpaceModelBase.metadata.tables[self.replica_config_model_name]
                .insert()
                .values(
                    deployment_id=deployment_id,
                    replicas=rc.replicas,
                    strategy=rc.strategy,
                    min_ready_seconds=rc.min_ready_seconds,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[
                        self.replica_config_model_name
                    ].c.id
                )
            )
            result = session.execute(rc_statement)
            rc_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        return rc_id

    def get_networking_config_model(self):
        class NetworkingConfig(ServiceSpaceModelBase):
            __tablename__ = self.networking_config_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            host_network = Column(Boolean, nullable=False)  # Use host network
            dns_policy = Column(String, nullable=False)  # DNS policy
            service_account_name = Column(String, nullable=True)  # Service account name

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "Deployment", back_populates=self.networking_config_model_name
            )

        return NetworkingConfig

    def _add_network_config_from_proto(
        self, nc: cpb2.NetworkingConfig, deployment_id: str
    ):
        """Add metadata and its labels/annotations from protobuf into the database."""
        # Populate deployment metadata
        with DbSession.session_scope() as session:
            nc_statement = (
                ServiceSpaceModelBase.metadata.tables[self.networking_config_model_name]
                .insert()
                .values(
                    deployment_id=deployment_id,
                    host_network=nc.host_network,
                    dns_policy=nc.dns_policy,
                    service_account_name=nc.service_account_name,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[
                        self.networking_config_model_name
                    ].c.id
                )
            )
            result = session.execute(nc_statement)
            nc_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        return nc_id

    def get_selector_model(self):
        class LabelSelector(ServiceSpaceModelBase):
            __tablename__ = self.selector_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            selector_labels = relationship(
                "SelectorLabels", back_populates=self.selector_model_name
            )
            selector_expressions = relationship(
                "SelectorExpressions", back_populates=self.selector_model_name
            )

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "Deployment", back_populates=self.selector_model_name
            )

        return LabelSelector

    def _add_selector_from_proto(self, ls: cpb2.LabelSelector, deployment_id: str):
        """Add metadata and its labels/annotations from protobuf into the database."""
        # Populate deployment metadata
        with DbSession.session_scope() as session:
            ls_statement = (
                ServiceSpaceModelBase.metadata.tables[self.selector_model_name]
                .insert()
                .values(
                    deployment_id=deployment_id,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[self.selector_model_name].c.id
                )
            )
            result = session.execute(ls_statement)
            ls_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        # Add labels
        with DbSession.session_scope() as session:
            for k, v in ls.match_labels.items():
                label_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.selector_labels_model_name
                    ]
                    .insert()
                    .values(
                        label_selector_id=ls_id,
                        key=k,
                        value=v,
                    )
                )
                session.execute(label_statement)
            session.commit()

        # Add annotations
        with DbSession.session_scope() as session:
            for expression in ls.match_expressions:
                expression_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.selector_expressions_model_name
                    ]
                    .insert()
                    .values(
                        label_selector_id=ls_id,
                        expression=expression,
                    )
                )
                session.execute(expression_statement)
            session.commit()

        return ls_id

    def get_selector_labels_model(self):
        class SelectorLabels(ServiceSpaceModelBase):
            __tablename__ = self.selector_labels_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            label_selector_id = Column(
                Integer, ForeignKey(f"{self.selector_model_name}.id")
            )
            key = Column(String, nullable=False)
            value = Column(String, nullable=False)

            # Many-to-One relationship with Deployment
            label_selector = relationship(
                "LabelSelector", back_populates=self.selector_labels_model_name
            )

        return SelectorLabels

    def get_selector_expressions_model(self):
        class SelectorExpressions(ServiceSpaceModelBase):
            __tablename__ = self.selector_expressions_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            label_selector_id = Column(
                Integer, ForeignKey(f"{self.selector_model_name}.id")
            )
            expression = Column(String, nullable=False)

            # Many-to-One relationship with LabelSelector
            label_selector = relationship(
                "LabelSelector", back_populates=self.selector_expressions_model_name
            )

        return SelectorExpressions

    def get_pod_template_model(self):
        class PodTemplate(ServiceSpaceModelBase):
            __tablename__ = self.pod_template_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            deployment_id = Column(
                String, ForeignKey(f"{self.deployment_model_name}.id")
            )
            labels = relationship(
                "PodTemplateLabels", back_populates=self.pod_template_model_name
            )
            annotations = relationship(
                "PodTemplateAnnotations", back_populates=self.pod_template_model_name
            )
            containers = relationship(
                "Container", back_populates=self.pod_template_model_name
            )
            volumes = relationship(
                "Volume", back_populates=self.pod_template_model_name
            )

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "Deployment", back_populates=self.pod_template_model_name
            )

        return PodTemplate

    def _add_pod_template_from_proto(self, pt: cpb2.PodTemplate, deployment_id: str):
        with DbSession.session_scope() as session:
            pt_statement = (
                ServiceSpaceModelBase.metadata.tables[self.pod_template_model_name]
                .insert()
                .values(
                    deployment_id=deployment_id,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[
                        self.pod_template_model_name
                    ].c.id
                )
            )
            result = session.execute(pt_statement)
            pt_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        # Add labels
        with DbSession.session_scope() as session:
            for k, v in pt.labels.items():
                label_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.template_labels_model_name
                    ]
                    .insert()
                    .values(
                        pod_template_id=pt_id,
                        key=k,
                        value=v,
                    )
                )
                session.execute(label_statement)
            session.commit()

        # Add annotations
        with DbSession.session_scope() as session:
            for k, v in pt.annotations.items():
                at_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.template_annotations_model_name
                    ]
                    .insert()
                    .values(
                        pod_template_id=pt_id,
                        key=k,
                        value=v,
                    )
                )
                session.execute(at_statement)
            session.commit()

        # Add containers
        for ct in pt.containers:
            self._add_template_container_from_proto(ct, pt_id)

        # Add volumes
        with DbSession.session_scope() as session:
            for volume in pt.volumes:
                v_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.template_volumes_model_name
                    ]
                    .insert()
                    .values(
                        pod_template_id=pt_id,
                        name=volume.name,
                        type=volume.type,
                        source=volume.source,
                    )
                )
                session.execute(v_statement)
            session.commit()

        return pt_id

    def get_template_labels_model(self):
        class PodTemplateLabels(ServiceSpaceModelBase):
            __tablename__ = self.template_labels_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            pod_template_id = Column(
                Integer, ForeignKey(f"{self.pod_template_model_name}.id")
            )
            key = Column(String, nullable=False)
            value = Column(String, nullable=False)

            # Many-to-One relationship with Deployment
            pod_template = relationship(
                "PodTemplate", back_populates=self.template_labels_model_name
            )

        return PodTemplateLabels

    def get_template_annotations_model(self):
        class PodTemplateAnnotations(ServiceSpaceModelBase):
            __tablename__ = self.template_annotations_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            pod_template_id = Column(
                Integer, ForeignKey(f"{self.pod_template_model_name}.id")
            )
            key = Column(String, nullable=False)
            value = Column(String, nullable=False)

            # Many-to-One relationship with Deployment
            pod_template = relationship(
                "PodTemplate", back_populates=self.template_annotations_model_name
            )

        return PodTemplateAnnotations

    def get_template_containers_model(self):
        class Container(ServiceSpaceModelBase):
            __tablename__ = self.template_containers_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            pod_template_id = Column(
                Integer, ForeignKey(f"{self.pod_template_model_name}.id")
            )
            name = Column(String, nullable=False)
            image = Column(String, nullable=False)
            commands = relationship(
                "ContainerCommand", back_populates=self.template_containers_model_name
            )
            args = relationship(
                "ContainerArgument", back_populates=self.template_containers_model_name
            )
            ports = relationship(
                "ContainerPort", back_populates=self.template_containers_model_name
            )
            envs = relationship(
                "EnvVar", back_populates=self.template_containers_model_name
            )
            requests = relationship(
                "ResourceRequests", back_populates=self.pod_template_model_name
            )
            limits = relationship(
                "ResourceLimits", back_populates=self.pod_template_model_name
            )

            # Many-to-One relationship with Deployment
            deployment = relationship(
                "PodTemplate", back_populates=self.template_containers_model_name
            )

        return Container

    def _add_template_container_from_proto(self, ct: cpb2.Container, pt_id: str):
        with DbSession.session_scope() as session:
            ct_statement = (
                ServiceSpaceModelBase.metadata.tables[
                    self.template_containers_model_name
                ]
                .insert()
                .values(
                    pod_template_id=pt_id,
                    name=ct.name,
                    image=ct.image,
                )
                .returning(
                    ServiceSpaceModelBase.metadata.tables[
                        self.template_containers_model_name
                    ].c.id
                )
            )
            result = session.execute(ct_statement)
            ct_id = result.scalar()  # Retrieve the auto-assigned ID
            session.commit()

        # Add commands
        with DbSession.session_scope() as session:
            for cmd in ct.command:
                cmd_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.container_command_model_name
                    ]
                    .insert()
                    .values(container_id=ct_id, command=cmd)
                )
                session.execute(cmd_statement)
            session.commit()

        # Add args
        with DbSession.session_scope() as session:
            for arg in ct.args:
                arg_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.template_annotations_model_name
                    ]
                    .insert()
                    .values(
                        container_id=ct_id,
                        argument=arg,
                    )
                )
                session.execute(arg_statement)
            session.commit()

        # Add ports
        with DbSession.session_scope() as session:
            for port in ct.ports:
                port_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.container_ports_model_name
                    ]
                    .insert()
                    .values(
                        container_id=ct_id,
                        name=port.name,
                        container_port=port.container_port,
                        protocol=port.protocol,
                    )
                )
                session.execute(port_statement)
            session.commit()

        # Add env_vars
        with DbSession.session_scope() as session:
            for env in ct.env_vars:
                env_statement = (
                    ServiceSpaceModelBase.metadata.tables[
                        self.container_envs_model_name
                    ]
                    .insert()
                    .values(
                        container_id=ct_id,
                        name=env.name,
                        value=env.value,
                    )
                )
                session.execute(env_statement)
            session.commit()

        # Add resource requests
        with DbSession.session_scope() as session:
            rr = ct.resource_requests
            rr_statement = (
                ServiceSpaceModelBase.metadata.tables[
                    self.container_requests_model_name
                ]
                .insert()
                .values(
                    container_id=ct_id,
                    cpu=rr.cpu,
                    memory=rr.memory,
                )
            )
            session.execute(rr_statement)
            session.commit()

        # Add resource limits
        with DbSession.session_scope() as session:
            rl = ct.resource_limits
            rl_statement = (
                ServiceSpaceModelBase.metadata.tables[self.container_limits_model_name]
                .insert()
                .values(
                    container_id=ct_id,
                    cpu=rl.cpu,
                    memory=rl.memory,
                )
            )
            session.execute(rl_statement)
            session.commit()

        return ct_id

    def get_containers_proto(self, pt_id: str) -> list:
        containers = []
        with DbSession.session_scope() as session:
            # Query the main container table
            containers_query = (
                session.query(self.template_containers_table)
                .filter(self.template_containers_table.c.pod_template_id == pt_id)
                .all()
            )

            for container_row in containers_query:
                container_id = container_row.id

                # Fetch commands
                commands_query = (
                    session.query(self.container_command_table)
                    .filter(self.container_command_table.c.container_id == container_id)
                    .all()
                )
                commands = [cmd.command for cmd in commands_query]

                # Fetch args
                args_query = (
                    session.query(self.container_args_table)
                    .filter(self.container_args_table.c.container_id == container_id)
                    .all()
                )
                args = [arg.argument for arg in args_query]

                # Fetch ports
                ports_query = (
                    session.query(self.container_ports_table)
                    .filter(self.container_ports_table.c.container_id == container_id)
                    .all()
                )
                ports = [
                    cpb2.ContainerPort(
                        id=f"{port.id}",
                        container_id=f"{container_id}",
                        name=port.name,
                        container_port=port.container_port,
                        protocol=port.protocol,
                    )
                    for port in ports_query
                ]

                # Fetch env vars
                env_vars_query = (
                    session.query(self.container_envs_table)
                    .filter(self.container_envs_table.c.container_id == container_id)
                    .all()
                )
                env_vars = [
                    cpb2.EnvVar(
                        id=f"{env.id}",
                        container_id=f"{container_id}",
                        name=env.name,
                        value=env.value,
                    )
                    for env in env_vars_query
                ]

                # Fetch resource requests
                requests_query = (
                    session.query(self.container_requests_table)
                    .filter(
                        self.container_requests_table.c.container_id == container_id
                    )
                    .first()
                )
                resource_requests = cpb2.ResourceRequests(
                    id=f"{requests_query.id}",
                    container_id=f"{container_id}",
                    cpu=requests_query.cpu,
                    memory=requests_query.memory,
                )

                # Fetch resource limits
                limits_query = (
                    session.query(self.container_limits_table)
                    .filter(self.container_limits_table.c.container_id == container_id)
                    .first()
                )
                resource_limits = cpb2.ResourceLimits(
                    id=f"{limits_query.id}",
                    container_id=f"{container_id}",
                    cpu=limits_query.cpu,
                    memory=limits_query.memory,
                )

                # Reconstruct the container proto
                container_proto = cpb2.Container(
                    id=f"{container_id}",
                    name=container_row.name,
                    image=container_row.image,
                    command=commands,
                    args=args,
                    ports=ports,
                    env_vars=env_vars,
                    resource_requests=resource_requests,
                    resource_limits=resource_limits,
                )

                containers.append(container_proto)

        return containers

    def get_template_volumes_model(self):
        class Volume(ServiceSpaceModelBase):
            __tablename__ = self.template_volumes_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            pod_template_id = Column(
                Integer, ForeignKey(f"{self.pod_template_model_name}.id")
            )
            name = Column(String, nullable=False)
            type = Column(String, nullable=False)
            source = Column(String, nullable=False)

            # Many-to-One relationship with Deployment
            pod_template = relationship(
                "PodTemplate", back_populates=self.template_volumes_model_name
            )

        return Volume

    def get_container_command_model(self):
        class ContainerCommand(ServiceSpaceModelBase):
            __tablename__ = self.container_command_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            command = Column(String, nullable=False)

            container = relationship(
                "Container", back_populates=self.container_command_model_name
            )

        return ContainerCommand

    def get_container_args_model(self):
        class ContainerArgument(ServiceSpaceModelBase):
            __tablename__ = self.container_args_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            argument = Column(String, nullable=False)

            container = relationship(
                "Container", back_populates=self.container_args_model_name
            )

        return ContainerArgument

    def get_container_ports_model(self):
        class ContainerPort(ServiceSpaceModelBase):
            __tablename__ = self.container_ports_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            name = Column(String, nullable=False)
            container_port = Column(Integer, nullable=False)
            protocol = Column(String, nullable=False)  # Could be 'TCP' or 'UDP'

            # Foreign key to a container (assuming a relationship exists)
            container = relationship(
                "Container", back_populates=self.container_ports_model_name
            )

        return ContainerPort

    def get_container_envs_model(self):
        class EnvVar(ServiceSpaceModelBase):
            __tablename__ = self.container_envs_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            name = Column(String, nullable=False)
            value = Column(String, nullable=False)

            # Foreign key to a container (assuming a relationship exists)
            container = relationship(
                "Container", back_populates=self.container_envs_model_name
            )

        return EnvVar

    def get_container_requests_model(self):
        class ResourceRequests(ServiceSpaceModelBase):
            __tablename__ = self.container_requests_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            cpu = Column(
                String, nullable=False
            )  # Could represent CPU allocation in millicores (e.g., '500m')
            memory = Column(
                String, nullable=False
            )  # Memory in a format like '512Mi', '1Gi'

            # Foreign key to a container (assuming a relationship exists)
            container = relationship(
                "Container", back_populates=self.container_requests_model_name
            )

        return ResourceRequests

    def get_container_limits_model(self):
        class ResourceLimits(ServiceSpaceModelBase):
            __tablename__ = self.container_limits_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            container_id = Column(
                Integer, ForeignKey(f"{self.template_containers_model_name}.id")
            )
            cpu = Column(
                String, nullable=False
            )  # Could represent CPU allocation in millicores (e.g., '500m')
            memory = Column(
                String, nullable=False
            )  # Memory in a format like '512Mi', '1Gi'

            # Foreign key to a container (assuming a relationship exists)
            container = relationship(
                "Container", back_populates=self.container_limits_model_name
            )

        return ResourceLimits
