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

class Registry(object):
    __services = dict()
    __data = dict()


    @staticmethod
    def register_service(name: str, service: object):
        if name in Registry.__services:
            raise RuntimeError('Service with name {0} already registered!'.format(name))

        Registry.__services[name] = service

    @staticmethod
    def get_service(name: object) -> object:
        if name in Registry.__services:
            return Registry.__services.get(name)
        return None

    @staticmethod
    def register_data(name: str, value: object):
        Registry.__data[name] = value

    @staticmethod
    def get_data(name: object) -> object:
        return Registry.__data.get(name)

    @staticmethod
    def delete_data(name: object) -> bool:
        if Registry.__data.get(name, False):
            Registry.__data.pop(name)
            return True
        else:
            return False