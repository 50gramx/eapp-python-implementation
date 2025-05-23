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
from community.gramx.fifty.zero.ethos.identity.entities.universe.discover.capabilities.discover_universe_service import \
    DiscoverUniverseService
from community.gramx.fifty.zero.ethos.identity.entities.universe.service.create_universe_service import \
    CreateUniverseService
from community.gramx.fifty.zero.ethos.identity.entities.universe.service.delete_universe_service import \
    DeleteUniverseService
from community.gramx.fifty.zero.ethos.identity.entities.universe.service.update_universe_service import \
    UpdateUniverseService
from support.application.registry import Registry


def register_universe_services(aio: bool):
    if aio:
        pass
    else:
        create_universe_service = CreateUniverseService()
        Registry.register_service('create_universe_service', create_universe_service)
        discover_universe_service = DiscoverUniverseService()
        Registry.register_service('discover_universe_service', discover_universe_service)
        update_universe_service = UpdateUniverseService()
        Registry.register_service('update_universe_service', update_universe_service)
        delete_universe_service = DeleteUniverseService()
        Registry.register_service('delete_universe_service', delete_universe_service)

    return
