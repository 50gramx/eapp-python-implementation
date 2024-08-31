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
import unicodedata
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, update, Float
from sqlalchemy.ext.declarative import declarative_base

from db_session import DbSession
# from ethos.elint.entities import space_knowledge_pb2, space_knowledge_domain_pb2, space_knowledge_domain_file_pb2, \
#     space_knowledge_domain_file_page_pb2, space_knowledge_domain_file_page_para_pb2
from ethos.elint.entities import space_things_pb2, space_things_domain_pb2, space_things_domain_device_pb2
from ethos.elint.entities.space_knowledge_domain_file_page_para_pb2 import PageContourDimensions
from support.helper_functions import format_timestamp_to_datetime, get_current_timestamp, gen_uuid, \
    format_datetime_to_timestamp

ThingsSpaceModels = declarative_base()


class ThingsSpace:
    def __init__(self, space_things_id: str):
        self.space_things_id = space_things_id
        self.domain_model_name = f"std_{space_things_id}"
        ThingsSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.domain_table = ThingsSpaceModels.metadata.tables[self.domain_model_name]
        except KeyError:
            self.domain_table = None

    # Setup Things Space
    def setup_things_space(self):
        self.get_domain_model().__table__.create(bind=DbSession.get_engine())
        return

    # Domain
    def get_domain_model(self):
        class SpaceThingsDomain(ThingsSpaceModels):
            __tablename__ = self.domain_model_name

            space_things_domain_id = Column(String(255), primary_key=True, unique=True)
            space_things_domain_name = Column(String(255), nullable=False)
            space_things_domain_description = Column(String(255), nullable=True)
            space_things_domain_collar_enum = Column(Integer, nullable=False)
            space_things_domain_isolated = Column(Boolean(), nullable=False)
            space_things_id = Column(String(255), nullable=False)
            created_at = Column(DateTime(), nullable=False)
            last_updated_at = Column(DateTime(), nullable=False)
            # TODO(@peivee): fix params

        return SpaceThingsDomain

    def get_domain_model_name(self):
        return self.domain_model_name

    def add_new_domain(self, domain_name: str, domain_description: str, domain_collar_enum: int,
                       domain_isolate: bool) -> str:
        domain_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.domain_model_name].insert().values(
            id=domain_id,
            name=domain_name,
            description=domain_description,
            collar_enum=domain_collar_enum,
            is_isolated=domain_isolate,
            space_things_id=self.space_things_id,
            created_at=format_timestamp_to_datetime(get_current_timestamp()),
            last_updated_at=format_timestamp_to_datetime(get_current_timestamp()),
        )   # TODO(@peivee): fix params
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        domain_things_space = DomainThingsSpace(space_things_id=self.space_things_id,
                                                      space_things_domain_id=domain_id)
        domain_things_space.setup_domain_things_space()
        return domain_id

    def get_domain_with_id(
            self,
            space_things: space_things_pb2.SpaceThings,
            domain_id: str
    ) -> space_things_domain_pb2.SpaceThingsDomain:
        with DbSession.session_scope() as session:
            if domain_id != "":
                space_things_domain = session.query(self.domain_table).filter(
                    self.domain_table.c.space_things_domain_id == domain_id
                ).first()
            else:
                space_things_domain = session.query(self.domain_table).filter(
                    self.domain_table.c.space_things_domain_collar_enum == 0
                ).first()
                # TODO(@peivee): fix this
            if space_things_domain is None:
                return space_things_domain_pb2.SpaceThingsDomain()
            else:
                return space_things_domain_pb2.SpaceThingsDomain(
                    id=space_things_domain.id,
                )   # TODO(@peivee): remaining things

    def get_domain_all(self, space_things: space_things_pb2.SpaceThings):
        with DbSession.session_scope() as session:
            space_things_domains = session.query(self.domain_table).all()
            return [space_things_domain_pb2.SpaceThingsDomain(
                space_things_domain_id=space_things_domain.space_things_domain_id,
            ) for space_things_domain in space_things_domains]    # TODO(@peivee): fix remaining

    # TODO(@peivee): fix this - DONE
    def update_domain_last_updated_at(self, space_things_domain_id: str):
        statement = (update(self.domain_table).where(
            self.domain_table.c.space_things_domain_id == space_things_domain_id).values(
            last_updated_at=format_timestamp_to_datetime(get_current_timestamp())))
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return



# TODO (@peivee): please try to understand this
# Like in knowledge domain, have file, page and para defined..
# Similarly, in things domain, has device defined..
class DomainThingsSpace:

    # TODO (@peivee): please try to relate why there are different tables with same id
    # I hope you will be able to visualise the distributed database architecture with domains
    def __init__(self, space_things_id: str, things_domain_id: str):
        self.space_things_domain_id = things_domain_id
        self.things_model_name = f"things_{things_domain_id}"
        self.domain_model_name = ThingsSpace(space_things_id=space_things_id).get_domain_model_name()
        self.machine_class_model_name = f"machine_class_{things_domain_id}"
        self.storage_class_model_name = f"storage_class_{things_domain_id}"
        self.bandwidth_class_model_name = f"bandwidth_class_{things_domain_id}"
        self.operator_class_model_name = f"operator_class_{things_domain_id}"
        self.hashing_class_model_name = f"hashing_class_{things_domain_id}"
        self.base_os_model_name = f"base_os_{things_domain_id}"
        self.orchestrator_os_model_name = f"orchestrator_os_{things_domain_id}"
        self.node_liability_model_name = f"node_liability_{things_domain_id}"
        self.ovpn_config_model_name = f"ovpn_config_{things_domain_id}"
        ThingsSpaceModels.metadata.reflect(bind=DbSession.get_engine())
        try:
            self.things_table = ThingsSpaceModels.metadata.tables[self.things_model_name]
            self.machine_class_table = ThingsSpaceModels.metadata.tables[self.machine_class_model_name]
            self.storage_class_table = ThingsSpaceModels.metadata.tables[self.storage_class_model_name]
            self.bandwidth_class_table = ThingsSpaceModels.metadata.tables[self.bandwidth_class_model_name]
            self.operator_class_table = ThingsSpaceModels.metadata.tables[self.operator_class_model_name]
            self.hashing_class_table = ThingsSpaceModels.metadata.tables[self.hashing_class_model_name]
            self.base_os_table = ThingsSpaceModels.metadata.tables[self.base_os_model_name]
            self.orchestrator_os_table = ThingsSpaceModels.metadata.tables[self.orchestrator_os_model_name]
            self.node_liability_table = ThingsSpaceModels.metadata.tables[self.node_liability_model_name]
            self.ovpn_config_table = ThingsSpaceModels.metadata.tables(self.ovpn_config_model_name)
        except KeyError:
            self.things_table = None
            self.machine_class_table = None
            self.storage_class_table = None
            self.bandwidth_class_table = None
            self.operator_class_table = None
            self.hashing_class_table = None
            self.base_os_table = None
            self.orchestrator_os_table = None
            self.node_liability_table = None
            self.ovpn_config_table = None

    # TODO(@peivee): here, all the base tables are setup
    # Setup Domain Knowledge Space
    def setup_domain_things_space(self):
        self.get_things_model().__table__.create(bind=DbSession.get_engine())
        self.get_machine_class_model().__table__.create(bind=DbSession.get_engine())
        self.get_storage_class_model().__table__.create(bind=DbSession.get_engine())
        self.get_bandwidth_class_model().__table__.create(bind=DbSession.get_engine())
        self.get_operator_class_model().__table__.create(bind=DbSession.get_engine())
        self.get_hashing_class_model().__table__.create(bind=DbSession.get_engine())
        self.get_base_os_model().__table__.create(bind=DbSession.get_engine())
        self.get_orchestrator_os_model().__table__.create(bind=DbSession.get_engine())
        self.get_node_liability_model().__table__.create(bind=DbSession.get_engine())
        self.get_ovpn_config_model().__table__.create(bind=DbSession.get_engine())
        return

    # Things Model
    def get_things_model(self):
        class ThingsModel(ThingsSpaceModels):
            __tablename__ = self.things_model_name

            node_id = Column(String(255), primary_key=True)
            name = Column(String(255), nullable=False)
            machine_class_id = Column(String(255), nullable=False)
            storage_class_id = Column(String(255), nullable=False)
            bandwidth_class_id = Column(String(255), nullable=False)
            operator_class_id = Column(String(255), nullable=False)
            hashing_class_id = Column(String(255), nullable=False)
            base_os_id = Column(String(255), nullable=False)
            orchestrator_os_id = Column(String(255), nullable=False)
            node_liability_id = Column(String(255), nullable=False)
            created_at = Column(DateTime, nullable=False)
        return ThingsModel


    def get_things_model_name(self):
        return self.things_model_name

    def add_new_thing(self, node_id: str, name: str, machine_class_id: str, storage_class_id: str,
                  bandwidth_class_id: str, operator_class_id: str, hashing_class_id: str, 
                  base_os_id: str, orchestrator_os_id: str, node_liability_id: str):
        statement = ThingsSpaceModels.metadata.tables[self.things_model_name].insert().values(
            node_id=node_id,
            name=name,
            machine_class_id=machine_class_id,
            storage_class_id=storage_class_id,
            bandwidth_class_id=bandwidth_class_id,
            operator_class_id=operator_class_id,
            hashing_class_id=hashing_class_id,
            base_os_id=base_os_id,
            orchestrator_os_id=orchestrator_os_id,
            node_liability_id=node_liability_id,
            created_at=format_timestamp_to_datetime(get_current_timestamp())
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return
    
    def get_thing_by_id(self, node_id: str):
        with DbSession.session_scope() as session:
            thing = session.query(self.get_things_model()).filter_by(node_id=node_id).first()
            if thing:
                return {
                    "node_id": thing.node_id,
                    "name": thing.name,
                    "machine_class_id": thing.machine_class_id,
                    "storage_class_id": thing.storage_class_id,
                    "bandwidth_class_id": thing.bandwidth_class_id,
                    "operator_class_id": thing.operator_class_id,
                    "hashing_class_id": thing.hashing_class_id,
                    "base_os_id": thing.base_os_id,
                    "orchestrator_os_id": thing.orchestrator_os_id,
                    "node_liability_id": thing.node_liability_id,
                    "created_at": format_datetime_to_timestamp(thing.created_at)
                }
            return None
    
    def list_all_things(self):
        with DbSession.session_scope() as session:
            things = session.query(self.get_things_model()).all()
            things_list = []
            for thing in things:
                things_list.append({
                    "node_id": thing.node_id,
                    "name": thing.name,
                    "machine_class_id": thing.machine_class_id,
                    "storage_class_id": thing.storage_class_id,
                    "bandwidth_class_id": thing.bandwidth_class_id,
                    "operator_class_id": thing.operator_class_id,
                    "hashing_class_id": thing.hashing_class_id,
                    "base_os_id": thing.base_os_id,
                    "orchestrator_os_id": thing.orchestrator_os_id,
                    "node_liability_id": thing.node_liability_id,
                    "created_at": format_datetime_to_timestamp(thing.created_at)
                })
            return things_list




    # Machine Class Model
    def get_machine_class_model(self):
        class MachineClassModel(ThingsSpaceModels):
            __tablename__ = self.machine_class_model_name

            id = Column(String(255), primary_key=True, unique=True)
            main_class = Column(String(255), nullable=False)
            sub_classes = Column(String(255), nullable=True)
            vcpu = Column(Integer, nullable=False)
            ram_gib = Column(Float, nullable=False)
            machine_type = Column(String(255), nullable=False)
            machine_category = Column(String(255), nullable=False)

        return MachineClassModel


    def get_machine_class_model_name(self):
        return self.machine_class_model_name


    def add_new_machine_class(self, main_class: str, sub_classes: str, vcpu: int, ram_gib: float,
                          machine_type: str, machine_category: str) -> str:
        machine_class_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.machine_class_model_name].insert().values(
            id=machine_class_id,
            main_class=main_class,
            sub_classes=sub_classes,
            vcpu=vcpu,
            ram_gib=ram_gib,
            machine_type=machine_type,
            machine_category=machine_category
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return machine_class_id

    def get_machine_class_by_id(self, machine_class_id: str):
        with DbSession.session_scope() as session:
            machine_class = session.query(self.get_machine_class_model()).filter_by(id=machine_class_id).first()
            if machine_class:
                return {
                    "id": machine_class.id,
                    "main_class": machine_class.main_class,
                    "sub_classes": machine_class.sub_classes,
                    "vcpu": machine_class.vcpu,
                    "ram_gib": machine_class.ram_gib,
                    "machine_type": machine_class.machine_type,
                    "machine_category": machine_class.machine_category
                }
            return None
    
    def list_all_machine_classes(self):
        with DbSession.session_scope() as session:
            machine_classes = session.query(self.get_machine_class_model()).all()
            machine_classes_list = []
            for machine_class in machine_classes:
                machine_classes_list.append({
                    "id": machine_class.id,
                    "main_class": machine_class.main_class,
                    "sub_classes": machine_class.sub_classes,
                    "vcpu": machine_class.vcpu,
                    "ram_gib": machine_class.ram_gib,
                    "machine_type": machine_class.machine_type,
                    "machine_category": machine_class.machine_category
                })
            return machine_classes_list



    # Storage Class Model
    def get_storage_class_model(self):
        class StorageClassModel(ThingsSpaceModels):
            __tablename__ = self.storage_class_model_name

            id = Column(String(255), primary_key=True, unique=True)
            main_class = Column(String(255), nullable=False)
            sub_classes = Column(String(255), nullable=True)
            fast_storage = Column(Float, nullable=False)
            standard_storage = Column(Float, nullable=False)
            slow_storage = Column(Float, nullable=False)

        return StorageClassModel


    def get_storage_class_model_name(self):
        return self.storage_class_model_name


    def add_new_storage_class(self, main_class: str, sub_classes: str, fast_storage: float, standard_storage: float, slow_storage: float) -> str:
        storage_class_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.storage_class_model_name].insert().values(
            id=storage_class_id,
            main_class=main_class,
            sub_classes=sub_classes,
            fast_storage=fast_storage,
            standard_storage=standard_storage,
            slow_storage=slow_storage
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return storage_class_id
    
    def get_storage_class_by_id(self, storage_class_id: str):
        with DbSession.session_scope() as session:
            storage_class = session.query(self.get_storage_class_model()).filter_by(id=storage_class_id).first()
            if storage_class:
                return {
                    "id": storage_class.id,
                    "main_class": storage_class.main_class,
                    "sub_classes": storage_class.sub_classes,
                    "fast_storage": storage_class.fast_storage,
                    "standard_storage": storage_class.standard_storage,
                    "slow_storage": storage_class.slow_storage
                }
            return None

    def list_all_storage_classes(self):
        with DbSession.session_scope() as session:
            storage_classes = session.query(self.get_storage_class_model()).all()
            storage_classes_list = []
            for storage_class in storage_classes:
                storage_classes_list.append({
                    "id": storage_class.id,
                    "main_class": storage_class.main_class,
                    "sub_classes": storage_class.sub_classes,
                    "fast_storage": storage_class.fast_storage,
                    "standard_storage": storage_class.standard_storage,
                    "slow_storage": storage_class.slow_storage
                })
            return storage_classes_list


    # Bandwidth Class Model
    def get_bandwidth_class_model(self):
        class BandwidthClassModel(ThingsSpaceModels):
            __tablename__ = self.bandwidth_class_model_name

            id = Column(String(255), primary_key=True, unique=True)
            main_class = Column(String(255), nullable=False)
            sub_classes = Column(String(255), nullable=True)
            locale_network_bandwidth_class = Column(Float, nullable=False)
            main_network_bandwidth_class = Column(Float, nullable=False)
            main_network_bandwidth_static_address = Column(Boolean, nullable=False)

        return BandwidthClassModel

    def get_bandwidth_class_model_name(self):
        return self.bandwidth_class_model_name


    def add_new_bandwidth_class(self, main_class: str, sub_classes: str, locale_network_bandwidth_class: float, 
                            main_network_bandwidth_class: float, main_network_bandwidth_static_address: bool) -> str:
        bandwidth_class_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.bandwidth_class_model_name].insert().values(
            id=bandwidth_class_id,
            main_class=main_class,
            sub_classes=sub_classes,
            locale_network_bandwidth_class=locale_network_bandwidth_class,
            main_network_bandwidth_class=main_network_bandwidth_class,
            main_network_bandwidth_static_address=main_network_bandwidth_static_address
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return bandwidth_class_id

    def get_bandwidth_class_by_id(self, bandwidth_class_id: str):
        with DbSession.session_scope() as session:
            bandwidth_class = session.query(self.get_bandwidth_class_model()).filter_by(id=bandwidth_class_id).first()
            if bandwidth_class:
                return {
                    "id": bandwidth_class.id,
                    "main_class": bandwidth_class.main_class,
                    "sub_classes": bandwidth_class.sub_classes,
                    "locale_network_bandwidth_class": bandwidth_class.locale_network_bandwidth_class,
                    "main_network_bandwidth_class": bandwidth_class.main_network_bandwidth_class,
                    "main_network_bandwidth_static_address": bandwidth_class.main_network_bandwidth_static_address
                }
            return None
    
    def list_all_bandwidth_classes(self):
        with DbSession.session_scope() as session:
            bandwidth_classes = session.query(self.get_bandwidth_class_model()).all()
            bandwidth_classes_list = []
            for bandwidth_class in bandwidth_classes:
                bandwidth_classes_list.append({
                    "id": bandwidth_class.id,
                    "main_class": bandwidth_class.main_class,
                    "sub_classes": bandwidth_class.sub_classes,
                    "locale_network_bandwidth_class": bandwidth_class.locale_network_bandwidth_class,
                    "main_network_bandwidth_class": bandwidth_class.main_network_bandwidth_class,
                    "main_network_bandwidth_static_address": bandwidth_class.main_network_bandwidth_static_address
                })
            return bandwidth_classes_list




    # Operator Class Model
    def get_operator_class_model(self):
        class OperatorClassModel(ThingsSpaceModels):
            __tablename__ = self.operator_class_model_name

            id = Column(String(255), primary_key=True, unique=True)
            main_class = Column(String(255), nullable=False)
            sub_classes = Column(String(255), nullable=True)
            human_operator_class = Column(Boolean, nullable=False)
            collaborator_operator_class = Column(Boolean, nullable=False)
            certified_operator_class = Column(Boolean, nullable=False)

        return OperatorClassModel


    def get_operator_class_model_name(self):
        return self.operator_class_model_name


    def add_new_operator_class(self, main_class: str, sub_classes: str, human_operator_class: bool, 
                           collaborator_operator_class: bool, certified_operator_class: bool) -> str:
        operator_class_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.operator_class_model_name].insert().values(
            id=operator_class_id,
            main_class=main_class,
            sub_classes=sub_classes,
            human_operator_class=human_operator_class,
            collaborator_operator_class=collaborator_operator_class,
            certified_operator_class=certified_operator_class
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return operator_class_id
    
    def get_operator_class_by_id(self, operator_class_id: str):
        with DbSession.session_scope() as session:
            operator_class = session.query(self.get_operator_class_model()).filter_by(id=operator_class_id).first()
            if operator_class:
                return {
                    "id": operator_class.id,
                    "main_class": operator_class.main_class,
                    "sub_classes": operator_class.sub_classes,
                    "human_operator_class": operator_class.human_operator_class,
                    "collaborator_operator_class": operator_class.collaborator_operator_class,
                    "certified_operator_class": operator_class.certified_operator_class
                }
            return None
    
    def list_all_operator_classes(self):
        with DbSession.session_scope() as session:
            operator_classes = session.query(self.get_operator_class_model()).all()
            operator_classes_list = []
            for operator_class in operator_classes:
                operator_classes_list.append({
                    "id": operator_class.id,
                    "main_class": operator_class.main_class,
                    "sub_classes": operator_class.sub_classes,
                    "human_operator_class": operator_class.human_operator_class,
                    "collaborator_operator_class": operator_class.collaborator_operator_class,
                    "certified_operator_class": operator_class.certified_operator_class
                })
            return operator_classes_list




    # Hashing Class Model
    def get_hashing_class_model(self):
        class HashingClassModel(ThingsSpaceModels):
            __tablename__ = self.hashing_class_model_name

            id = Column(String(255), primary_key=True, unique=True)
            main_class = Column(String(255), nullable=False)
            sub_classes = Column(String(255), nullable=True)
            chain_hash_generation_class = Column(Boolean, nullable=False)

        return HashingClassModel


    def get_hashing_class_model_name(self):
        return self.hashing_class_model_name


    def add_new_hashing_class(self, main_class: str, sub_classes: str, chain_hash_generation_class: bool) -> str:
        hashing_class_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.hashing_class_model_name].insert().values(
            id=hashing_class_id,
            main_class=main_class,
            sub_classes=sub_classes,
            chain_hash_generation_class=chain_hash_generation_class
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return hashing_class_id
    
    def get_hashing_class_by_id(self, hashing_class_id: str):
        with DbSession.session_scope() as session:
            hashing_class = session.query(self.get_hashing_class_model()).filter_by(id=hashing_class_id).first()
            if hashing_class:
                return {
                    "id": hashing_class.id,
                    "main_class": hashing_class.main_class,
                    "sub_classes": hashing_class.sub_classes,
                    "chain_hash_generation_class": hashing_class.chain_hash_generation_class
                }
            return None
    
    def list_all_hashing_classes(self):
        with DbSession.session_scope() as session:
            hashing_classes = session.query(self.get_hashing_class_model()).all()
            hashing_classes_list = []
            for hashing_class in hashing_classes:
                hashing_classes_list.append({
                    "id": hashing_class.id,
                    "main_class": hashing_class.main_class,
                    "sub_classes": hashing_class.sub_classes,
                    "chain_hash_generation_class": hashing_class.chain_hash_generation_class
                })
            return hashing_classes_list




    # Base OS Model
    def get_base_os_model(self):
        class BaseOSModel(ThingsSpaceModels):
            __tablename__ = self.base_os_model_name

            id = Column(String(255), primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            arch = Column(String(255), nullable=False)

        return BaseOSModel


    def get_base_os_model_name(self):
        return self.base_os_model_name

    def add_new_base_os(self, name: str, arch: str) -> str:
        base_os_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.base_os_model_name].insert().values(
            id=base_os_id,
            name=name,
            arch=arch
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return base_os_id
    
    def get_base_os_by_id(self, base_os_id: str):
        with DbSession.session_scope() as session:
            base_os = session.query(self.get_base_os_model()).filter_by(id=base_os_id).first()
            if base_os:
                return {
                    "id": base_os.id,
                    "name": base_os.name,
                    "arch": base_os.arch
                }
            return None
    
    def list_all_base_os(self):
        with DbSession.session_scope() as session:
            base_os_list = session.query(self.get_base_os_model()).all()
            base_os_records = []
            for base_os in base_os_list:
                base_os_records.append({
                    "id": base_os.id,
                    "name": base_os.name,
                    "arch": base_os.arch
                })
            return base_os_records



    # Orchestrator OS Model
    def get_orchestrator_os_model(self):
        class OrchestratorOSModel(ThingsSpaceModels):
            __tablename__ = self.orchestrator_os_model_name

            id = Column(String(255), primary_key=True, unique=True)
            name = Column(String(255), nullable=False)
            version = Column(String(255), nullable=False)

        return OrchestratorOSModel


    def get_orchestrator_os_model_name(self):
        return self.orchestrator_os_model_name


    def add_new_orchestrator_os(self, name: str, version: str) -> str:
        orchestrator_os_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.orchestrator_os_model_name].insert().values(
            id=orchestrator_os_id,
            name=name,
            version=version
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return orchestrator_os_id
    
    def get_orchestrator_os_by_id(self, orchestrator_os_id: str):
        with DbSession.session_scope() as session:
            orchestrator_os = session.query(self.get_orchestrator_os_model()).filter_by(id=orchestrator_os_id).first()
            if orchestrator_os:
                return {
                    "id": orchestrator_os.id,
                    "name": orchestrator_os.name,
                    "version": orchestrator_os.version
                }
            return None
    
    def list_all_orchestrator_os(self):
        with DbSession.session_scope() as session:
            orchestrator_os_list = session.query(self.get_orchestrator_os_model()).all()
            orchestrator_os_records = []
            for orchestrator_os in orchestrator_os_list:
                orchestrator_os_records.append({
                    "id": orchestrator_os.id,
                    "name": orchestrator_os.name,
                    "version": orchestrator_os.version
                })
            return orchestrator_os_records




    # Node Liability Model
    def get_node_liability_model(self):
        class NodeLiabilityModel(ThingsSpaceModels):
            __tablename__ = self.node_liability_model_name

            id = Column(String(255), primary_key=True, unique=True)
            liability = Column(String(255), nullable=False)
            license_id = Column(String(255), nullable=True)

        return NodeLiabilityModel
    
    def get_node_liability_model_name(self):
        return self.node_liability_model_name

    def add_new_node_liability(self, liability: str, license_id: str) -> str:
        node_liability_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.node_liability_model_name].insert().values(
            id=node_liability_id,
            liability=liability,
            license_id=license_id
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return node_liability_id

    def get_node_liability_by_id(self, node_liability_id: str):
        with DbSession.session_scope() as session:
            node_liability = session.query(self.get_node_liability_model()).filter_by(id=node_liability_id).first()
            if node_liability:
                return {
                    "id": node_liability.id,
                    "liability": node_liability.liability,
                    "license_id": node_liability.license_id
                }
            return None
    
    def list_all_node_liabilities(self):
        with DbSession.session_scope() as session:
            node_liability_list = session.query(self.get_node_liability_model()).all()
            node_liability_records = []
            for node_liability in node_liability_list:
                node_liability_records.append({
                    "id": node_liability.id,
                    "liability": node_liability.liability,
                    "license_id": node_liability.license_id
                })
            return node_liability_records


    # OVPNConfig Model
    def get_ovpn_config_model(self):
        class OVPNConfigModel(ThingsSpaceModels):
            __tablename__ = self.ovpn_config_model_name

            config_id = Column(String(255), primary_key=True, unique=True)
            server_address = Column(String(255), nullable=False)
            port = Column(String(10), nullable=False)
            protocol = Column(String(10), nullable=False)
            ca_cert = Column(Text, nullable=False)
            cert = Column(Text, nullable=False)
            key = Column(Text, nullable=False)
            dh_param = Column(Text, nullable=False)
            tls_auth_key = Column(Text, nullable=False)
            allowed_ips = Column(ARRAY(String(255)), nullable=False)
            created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
            updated_at = Column(DateTime, nullable=True)
            description = Column(String(1024), nullable=True)

        return OVPNConfigModel

    def get_ovpn_config_model_name(self):
        return self.ovpn_config_model_name

    def add_new_ovpn_config(self, server_address: str, port: str, protocol: str, ca_cert: str, cert: str, key: str,
                        dh_param: str, tls_auth_key: str, allowed_ips: list, description: str) -> str:
        config_id = gen_uuid()
        statement = ThingsSpaceModels.metadata.tables[self.ovpn_config_model_name].insert().values(
            config_id=config_id,
            server_address=server_address,
            port=port,
            protocol=protocol,
            ca_cert=ca_cert,
            cert=cert,
            key=key,
            dh_param=dh_param,
            tls_auth_key=tls_auth_key,
            allowed_ips=allowed_ips,
            created_at=datetime.utcnow(),
            description=description
        )
        with DbSession.session_scope() as session:
            session.execute(statement)
            session.commit()
        return config_id

    def get_ovpn_config_by_id(self, config_id: str):
        with DbSession.session_scope() as session:
            ovpn_config = session.query(self.get_ovpn_config_model()).filter_by(config_id=config_id).first()
            if ovpn_config:
                return {
                    "config_id": ovpn_config.config_id,
                    "server_address": ovpn_config.server_address,
                    "port": ovpn_config.port,
                    "protocol": ovpn_config.protocol,
                    "ca_cert": ovpn_config.ca_cert,
                    "cert": ovpn_config.cert,
                    "key": ovpn_config.key,
                    "dh_param": ovpn_config.dh_param,
                    "tls_auth_key": ovpn_config.tls_auth_key,
                    "allowed_ips": ovpn_config.allowed_ips,
                    "created_at": ovpn_config.created_at,
                    "updated_at": ovpn_config.updated_at,
                    "description": ovpn_config.description
                }
            return None

    def list_all_ovpn_configs(self):
        with DbSession.session_scope() as session:
            ovpn_config_list = session.query(self.get_ovpn_config_model()).all()
            ovpn_config_records = []
            for ovpn_config in ovpn_config_list:
                ovpn_config_records.append({
                    "config_id": ovpn_config.config_id,
                    "server_address": ovpn_config.server_address,
                    "port": ovpn_config.port,
                    "protocol": ovpn_config.protocol,
                    "ca_cert": ovpn_config.ca_cert,
                    "cert": ovpn_config.cert,
                    "key": ovpn_config.key,
                    "dh_param": ovpn_config.dh_param,
                    "tls_auth_key": ovpn_config.tls_auth_key,
                    "allowed_ips": ovpn_config.allowed_ips,
                    "created_at": ovpn_config.created_at,
                    "updated_at": ovpn_config.updated_at,
                    "description": ovpn_config.description
                })
            return ovpn_config_records
