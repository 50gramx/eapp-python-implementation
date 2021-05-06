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
from ethos.elint.entities.machine_pb2 import Machine, MachineClassEnum, MachineNameEnum, MachineTypeEnum

"""
message Machine {
  string machine_id = 1;
  MachineClassEnum machine_class_enum = 2;
  MachineNameEnum machine_name_enum = 3;
  MachineTypeEnum machine_type_enum = 4;
  bool can_be_shared = 5;
  double hourly_rate = 6;
}
"""

all_machine_data_dump = [
    Machine(
        machine_id="m001",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.NANO,
        can_be_shared=False,
        hourly_rate=0.196
    ),
    Machine(
        machine_id="m002",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.MICRO,
        can_be_shared=False,
        hourly_rate=0.392
    ),
    Machine(
        machine_id="m003",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.SMALL,
        can_be_shared=False,
        hourly_rate=0.784
    ),
    Machine(
        machine_id="m004",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.MEDIUM,
        can_be_shared=False,
        hourly_rate=1.568
    )
    ,
    Machine(
        machine_id="m005",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.LARGE,
        can_be_shared=False,
        hourly_rate=3.136
    ),
    Machine(
        machine_id="m006",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.XLARGE,
        can_be_shared=False,
        hourly_rate=6.272
    ),
    Machine(
        machine_id="m007",
        machine_class_enum=MachineClassEnum.GENERAL,
        machine_name_enum=MachineNameEnum.X2,
        machine_type_enum=MachineTypeEnum.XXLARGE,
        can_be_shared=False,
        hourly_rate=12.544
    )
]


def get_all_machines() -> [Machine]:
    return all_machine_data_dump
