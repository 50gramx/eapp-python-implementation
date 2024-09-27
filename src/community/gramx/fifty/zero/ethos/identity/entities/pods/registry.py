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

from community.gramx.fifty.zero.ethos.identity.entities.pods.create.capabilities.implementation.create_pods_impl import CreatePodsService

from support.application.registry import Registry


def register_pod_services(aio: bool):
    if aio:
        pass
    else:
        print("registering pod services")
        create_pod_service = CreatePodsService()
        Registry.register_service('create_pods_service', create_pod_service)
    return
