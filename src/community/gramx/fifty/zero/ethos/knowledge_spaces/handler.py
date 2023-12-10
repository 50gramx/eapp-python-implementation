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

from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge.handler import \
    handle_space_knowledge_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain.handler import \
    handle_space_knowledge_domain_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.handler import \
    handle_space_knowledge_domain_file_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page.handler import \
    handle_space_knowledge_domain_file_page_services
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file_page_para.handler import \
    handle_space_knowledge_domain_file_page_para_services


def handle_knowledge_spaces_services(server):
    handle_space_knowledge_services(server)
    logging.info(f'\t [x] added space knowledge services')
    handle_space_knowledge_domain_services(server)
    logging.info(f'\t [x] added space knowledge domain services')
    handle_space_knowledge_domain_file_services(server)
    logging.info(f'\t [x] added space knowledge domain file services')
    handle_space_knowledge_domain_file_page_services(server)
    logging.info(f'\t [x] added space knowledge domain file page services')
    handle_space_knowledge_domain_file_page_para_services(server)
    logging.info(f'\t [x] added space knowledge domain file page para services')
    logging.info(f'Knowledge Spaces services added')
