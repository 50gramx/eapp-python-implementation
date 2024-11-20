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

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db_session import DbSession
from src.community.gramx.fifty.zero.ethos.service_spaces.models.base import (
    ServiceSpaceModelBase,
)


class DC499999998Model:
    def __init__(
        self,
        space_service_domain_id: str,
        space_service_domain_collar_code: str,
    ):
        self.space_service_domain_id = space_service_domain_id

        self.vm_instance_model_name = (
            f"{space_service_domain_collar_code}_5000_{space_service_domain_id}"
        )
        self.usage_metric_model_name = (
            f"{space_service_domain_collar_code}_5001_{space_service_domain_id}"
        )
        self.alerts_model_name = (
            f"{space_service_domain_collar_code}_5002_{space_service_domain_id}"
        )
        self.collar_model_name = (
            f"{space_service_domain_collar_code}_9999_{space_service_domain_id}"
        )
        try:
            self.collar_table = ServiceSpaceModelBase.metadata.tables[
                self.collar_model_name
            ]
            self.vm_instance_table = ServiceSpaceModelBase.metadata.tables[
                self.vm_instance_model_name
            ]
            self.usage_metric_table = ServiceSpaceModelBase.metadata.tables[
                self.usage_metric_model_name
            ]
            self.alerts_table = ServiceSpaceModelBase.metadata.tables[
                self.alerts_model_name
            ]
        except KeyError:
            self.collar_table = None
            self.vm_instance_table = None
            self.usage_metric_table = None
            self.alerts_table = None

    # Setup Domain Service Space
    def setup_domain_collar_service_space(self):
        self.get_vm_instance_model().__table__.create(bind=DbSession.get_engine())
        self.get_usage_metric_model().__table__.create(bind=DbSession.get_engine())
        self.get_alerts_model().__table__.create(bind=DbSession.get_engine())
        self.get_DC499999998_collar_model().__table__.create(
            bind=DbSession.get_engine()
        )
        return

    def get_DC499999998_collar_model(self):
        class DC499999998(ServiceSpaceModelBase):
            __tablename__ = self.collar_model_name

            id = Column(String, primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            description = Column(String)

            # One-to-One relationship with VMInstance
            vm_instance_id = Column(
                String, ForeignKey(f"{self.vm_instance_model_name}.id")
            )
            vm_instance = relationship(
                "VMInstance", back_populates=f"{self.collar_model_name}", uselist=False
            )

            created_at = Column(DateTime(), nullable=False)
            updated_at = Column(DateTime(), nullable=False)

        return DC499999998

    def get_vm_instance_model(self):
        class VMInstance(ServiceSpaceModelBase):
            __tablename__ = self.vm_instance_model_name

            id = Column(String, primary_key=True)
            collar_id = Column(String, nullable=False)
            pod_id = Column(String, nullable=False)
            cpu_cores = Column(Integer, nullable=False)
            ram_gb = Column(Float, nullable=False)
            storage_gb = Column(Float, nullable=False)
            status = Column(String, nullable=False)
            created_at = Column(DateTime(), nullable=False)
            updated_at = Column(DateTime())

            # One-to-One relationship with Service
            service = relationship(
                "DC499999998", back_populates=self.vm_instance_model_name
            )

            # One-to-Many relationship with UsageMetric
            usage_metrics = relationship(
                "UsageMetric", back_populates=self.vm_instance_model_name
            )

            # One-to-Many relationship with Alert
            alerts = relationship("Alert", back_populates=self.vm_instance_model_name)

        return VMInstance

    def get_usage_metric_model(self):
        class UsageMetric(ServiceSpaceModelBase):
            __tablename__ = self.usage_metric_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            vm_instance_id = Column(
                String, ForeignKey(f"{self.vm_instance_model_name}.id")
            )
            cpu_usage = Column(Float, nullable=False)
            memory_usage = Column(Float, nullable=False)
            disk_io = Column(Float, nullable=False)
            timestamp = Column(DateTime, nullable=False)

            # Many-to-One relationship with VMInstance
            vm_instance = relationship(
                "VMInstance", back_populates=self.usage_metric_model_name
            )

        return UsageMetric

    def get_alerts_model(self):
        class Alert(ServiceSpaceModelBase):
            __tablename__ = self.alerts_model_name

            id = Column(Integer, primary_key=True, autoincrement=True)
            vm_instance_id = Column(
                String, ForeignKey(f"{self.vm_instance_model_name}.id")
            )
            alert_type = Column(String, nullable=False)
            alert_message = Column(String, nullable=False)
            created_at = Column(DateTime, nullable=False)
            resolved_at = Column(DateTime)

            # Many-to-One relationship with VMInstance
            vm_instance = relationship(
                "VMInstance", back_populates=self.alerts_model_name
            )

        return Alert
