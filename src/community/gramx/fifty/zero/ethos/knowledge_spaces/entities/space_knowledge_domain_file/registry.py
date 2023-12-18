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
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.access.capabilities.access_space_knowledge_domain_file_service import \
    AccessSpaceKnowledgeDomainFileService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.create.capabilities.create_space_knowledge_domain_file_service import \
    CreateSpaceKnowledgeDomainFileService
from community.gramx.fifty.zero.ethos.knowledge_spaces.entities.space_knowledge_domain_file.delete.capabilities.delete_space_knowledge_domain_file_service import \
    DeleteSpaceKnowledgeDomainFileService
from support.application.registry import Registry


def register_space_knowledge_domain_file_services(aio: bool):
    if aio:
        pass
    else:
        create_space_knowledge_domain_file_service = CreateSpaceKnowledgeDomainFileService()
        Registry.register_service('create_space_knowledge_domain_file_service',
                                  create_space_knowledge_domain_file_service)
        access_space_knowledge_domain_file_service = AccessSpaceKnowledgeDomainFileService()
        Registry.register_service('access_space_knowledge_domain_file_service',
                                  access_space_knowledge_domain_file_service)
        delete_space_knowledge_domain_file_service = DeleteSpaceKnowledgeDomainFileService()
        Registry.register_service('delete_space_knowledge_domain_file_service',
                                  delete_space_knowledge_domain_file_service)
