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

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer, Float 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
50GRAMX Chains
"""


class Account(Base):
    __tablename__ = 'account'

    account_analytics_id = Column(String(255), primary_key=True, unique=True)
    account_id = Column(String(255), primary_key=True, unique=True)
    account_personal_email_id = Column(String(255), nullable=True, unique=True)
    account_work_email_id = Column(String(255), nullable=True, unique=True)
    account_country_code = Column(String(6), nullable=False)
    account_mobile_number = Column(String(10), nullable=False, unique=True)
    account_first_name = Column(String(40), nullable=False)
    account_last_name = Column(String(40), nullable=False)
    account_gender = Column(String(10), nullable=False)
    account_birth_at = Column(DateTime(), nullable=False)
    account_galaxy_id = Column(String(255), ForeignKey('galaxy.galaxy_id'), nullable=False)
    account_created_at = Column(DateTime(), nullable=False)
    account_billing_active = Column(Boolean())


class AccountDevices(Base):
    __tablename__ = 'account_devices'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True)
    account_device_os = Column(Integer(), nullable=False)
    account_device_token = Column(String(255), unique=True, nullable=False)
    account_device_token_accessed_at = Column(DateTime(), nullable=False)


class AccountSecrets(Base):
    __tablename__ = 'account_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_password = Column(String(255), nullable=False)
    account_password_last_updated_geo_lat = Column(String(255), nullable=False)
    account_password_last_updated_geo_long = Column(String(255), nullable=False)
    account_password_last_updated_at = Column(DateTime())
    account_password_created_at = Column(DateTime(), nullable=False)


class AccountConvenienceSecrets(Base):
    __tablename__ = 'account_convenience_secrets'

    account_id = Column(String(255), ForeignKey('account.account_id'), primary_key=True, unique=True)
    account_convenience_pin = Column(String(6), nullable=False)
    account_convenience_pin_created_at = Column(DateTime(), nullable=False)


class Universe(Base):
    __tablename__ = "universe"

    universe_id = Column(String(255), primary_key=True, unique=True)
    universe_name = Column(String(255), nullable=False, unique=True)
    universe_description = Column(String(255), nullable=False)
    universe_created_at = Column(DateTime(), nullable=False)
    universe_updated_at = Column(DateTime())


class Galaxy(Base):
    __tablename__ = "galaxy"

    galaxy_id = Column(String(255), primary_key=True, unique=True)
    galaxy_name = Column(String(255), nullable=False)
    universe_id = Column(String(255), ForeignKey('universe.universe_id'), nullable=False)
    galaxy_created_at = Column(DateTime(), nullable=False)


class Space(Base):
    __tablename__ = "space"

    space_id = Column(String(255), primary_key=True, unique=True)
    space_admin_id = Column(String(255), ForeignKey('account.account_id'), nullable=False)
    galaxy_id = Column(String(255), ForeignKey('galaxy.galaxy_id'), nullable=False)
    space_accessibility_type = Column(String(), nullable=False)
    space_isolation_type = Column(String(), nullable=False)
    space_entity_type = Column(String(), nullable=False)
    space_created_at = Column(DateTime(), nullable=False)


class AccountAssistant(Base):
    __tablename__ = "account_assistant"

    account_assistant_id = Column(String(255), primary_key=True)
    account_assistant_name_code = Column(Integer(), nullable=False)
    account_assistant_name = Column(String(255), nullable=False)
    account_id = Column(String(255), ForeignKey('account.account_id'))
    created_at = Column(DateTime(), nullable=False)
    last_assisted_at = Column(DateTime(), nullable=False)


class AccountAssistantNameCode(Base):
    __tablename__ = "account_assistant_name_code"

    account_assistant_name = Column(String(255), primary_key=True)
    account_assistant_name_code = Column(Integer(), primary_key=True)
    account_id = Column(String(255), primary_key=True)


class CoreCollaborator(Base):
    __tablename__ = "core_collaborator"

    collaborator_first_name = Column(String(255), primary_key=True)
    collaborator_last_name = Column(String(255), primary_key=True)
    collaborator_community_code = Column(Integer(), primary_key=True)

class SpaceThings(Base):
    __tablename__ = "space_things"

    space_things_id         = Column(String(255), primary_key=True)  
    space_things_name       = Column(String(255), nullable=False)
    space_things_admin_id   = Column(String(255), ForeignKey('account.account_id'), nullable=False)
    space_things_space_id   = Column(String(255), ForeignKey('space.space_id'), nullable=False)
    space_things_created_at = Column(DateTime(), nullable=False)


class MachineClass(Base):
    __tablename__ = 'machine_class'
    
    machine_class_id                = Column(String(255), primary_key=True)
    machine_class_main_class        = Column(String(255), nullable=False)
    machine_class_sub_classes       = Column(String(255), nullable=False)
    machine_class_vcpu              = Column(Integer(), nullable=False)
    machine_class_ram_gib           = Column(Float(), nullable=False)
    machine_class_machine_type      = Column(String(255), nullable=False)
    machine_class_machine_category  = Column(String(255), nullable=False)

class StorageClass(Base):
    __tablename__ = 'storage_class'
    
    storage_class_id                = Column(String(255), primary_key=True)
    storage_class_main_class        = Column(String(255), nullable=False)
    storage_class_sub_classes       = Column(String(255), nullable=False)
    storage_class_fast_storage      = Column(Float(), nullable=False)
    storage_class_standard_storage  = Column(Float(), nullable=False)
    storage_class_slow_storage      = Column(Float(), nullable=False)

class BandwidthClass(Base):
    __tablename__ = 'bandwidth_class'
    
    bandwidth_class_id                                      = Column(String(255), primary_key=True)
    bandwidth_class_main_class                              = Column(String(255), nullable=False)
    bandwidth_class_sub_classes                             = Column(String(255), nullable=False)
    bandwidth_class_locale_network_bandwidth_class          = Column(Float(), nullable=False)
    bandwidth_class_main_network_bandwidth_class            = Column(Float(), nullable=False)
    bandwidth_class_main_network_bandwidth_static_address   = Column(Boolean(), nullable=False)

class OperatorClass(Base):
    __tablename__ = 'operator_class'
    
    operator_class_id                           = Column(String(255), primary_key=True)
    operator_class_main_class                   = Column(String(255), nullable=False)
    operator_class_sub_classes                  = Column(String(255), nullable=False)
    operator_class_human_operator_class         = Column(Boolean(), nullable=False)
    operator_class_collaborator_operator_class  = Column(Boolean(), nullable=False)
    operator_class_certified_operator_class     = Column(Boolean(), nullable=False)

class HashingClass(Base):
    __tablename__ = 'hashing_class'
    
    hashing_class_id                            = Column(String(255), primary_key=True)
    hashing_class_main_class                    = Column(String(255), nullable=False)
    hashing_class_sub_classes                   = Column(String(255), nullable=False)
    hashing_class_chain_hash_generation_class   = Column(Boolean(), nullable=False)

class OrchestratorOS(Base):
    __tablename__ = 'orchestrator_os'
    
    orchestrator_os_id      = Column(String(255), primary_key=True)
    orchestrator_os_name    = Column(String(255), nullable=False)
    orchestrator_os_version = Column(String(255), nullable=False)

class NodeLiability(Base):
    __tablename__ = 'node_liability'
    
    node_liability_id           = Column(String(255), primary_key=True)
    node_liability_liability    = Column(String(255), nullable=False)
    node_liability_license_id   = Column(String(255), nullable=False)

class Things50DC500000000(Base):
    __tablename__ = 'things_50dc500000000'
    
    things_50dc500000000_node_id            = Column(String(255), primary_key=True)
    things_50dc500000000_name               = Column(String(255), nullable=False)
    things_50dc500000000_machine_class_id   = Column(String(255), ForeignKey('machine_class.machine_class_id'), nullable=False)
    things_50dc500000000_storage_class_id   = Column(String(255), ForeignKey('storage_class.storage_class_id'), nullable=False)
    things_50dc500000000_bandwidth_class_id = Column(String(255), ForeignKey('bandwidth_class.bandwidth_class_id'), nullable=False)
    things_50dc500000000_operator_class_id  = Column(String(255), ForeignKey('operator_class.operator_class_id'), nullable=False)
    things_50dc500000000_hashing_class_id   = Column(String(255), ForeignKey('hashing_class.hashing_class_id'), nullable=False)
    things_50dc500000000_base_os_id         = Column(String(255), ForeignKey('base_os.base_os_id'), nullable=False)
    things_50dc500000000_orchestrator_os_id = Column(String(255), ForeignKey('orchestrator_os.orchestrator_os_id'), nullable=False)
    things_50dc500000000_node_liability_id  = Column(String(255), ForeignKey('node_liability.node_liability_id'), nullable=False)
    things_50dc500000000_created_at         = Column(DateTime(), nullable=False)