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


from community.gramx.fifty.zero.ethos.identity.entities.galaxy.service.create_galaxy_service import CreateGalaxyService
from community.gramx.fifty.zero.ethos.identity.entities.galaxy.service.read_galaxy_service import ReadGalaxyService
from community.gramx.fifty.zero.ethos.identity.entities.galaxy.service.update_galaxy_service import UpdateGalaxyService
from community.gramx.fifty.zero.ethos.identity.entities.galaxy.service.delete_galaxy_service import DeleteGalaxyService

from support.application.registry import Registry


def register_account_services(aio: bool):
    if aio:
        pass
    else:
        create_galaxy_service = CreateGalaxyService()
        Registry.register_service('create_galaxy_service', create_galaxy_service)
        read_galaxy_service = ReadGalaxyService()
        Registry.register_service('read_galaxy_service', read_galaxy_service)
        update_galaxy_service = UpdateGalaxyService()
        Registry.register_service('update_galaxy_service', update_galaxy_service)
        delete_galaxy_service = DeleteGalaxyService()
        Registry.register_service('delete_galaxy_service', delete_galaxy_service)

    return
