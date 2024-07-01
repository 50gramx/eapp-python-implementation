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

from community.gramx.fifty.zero.ethos.identity.entities.account.handler import handle_account_services
from community.gramx.fifty.zero.ethos.identity.entities.account_assistant.handler import \
    handle_account_assistant_services
from community.gramx.fifty.zero.ethos.identity.entities.space.handler import handle_space_services
from community.gramx.fifty.zero.ethos.identity.entities.universe.handler import handle_universe_services


def handle_identity_services(server, aio: bool):
    handle_universe_services(server=server, aio=aio)
    logging.info(f'\t [x] added universe services')
    handle_account_services(server, aio)
    logging.info(f'\t [x] added account services')
    handle_space_services(server, aio)
    logging.info(f'\t [x] added space services')
    handle_account_assistant_services(server, aio)
    logging.info(f'\t [x] added account assistant services')
    logging.info(f'Identity services added')
