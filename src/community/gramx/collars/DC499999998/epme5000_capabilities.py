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

from ethos.elint.collars.DC499999998_pb2 import LaunchVMResponse
from ethos.elint.collars.DC499999998_pb2_grpc import (
    DC499999998EPME5000CapabilitiesServicer,
)
from ethos.elint.collars.DC499999999_caps_pb2 import AuthWithDeployment
from ethos.elint.collars.DC499999999_pb2 import (
    Container,
    ContainerPort,
    Deployment,
    PodTemplate,
)

from src.community.gramx.collars.DC499999999.epme5000_consumer import (
    DC499999999EPME5000Consumer,
)
from support.application.tracing import trace_rpc


class DC499999998EPME5000Capabilities(DC499999998EPME5000CapabilitiesServicer):
    def __init__(self):
        super(DC499999998EPME5000Capabilities, self).__init__()
        self.session_scope = self.__class__.__name__

    @trace_rpc()
    def LaunchVM(self, request, context):
        logging.info(f"{self.session_scope}:LaunchVM")
        # Actually call the pod deployment
        # wait for the pod deployment
        # once done, add the VM details from deployed pod to the db
        # return values
        #     final Map<String, dynamic> podData = {
        #   'name': podName,
        #   'image': image,
        #   'container_ports': containerPorts.map((port) => port['port']).toList(),
        #   'env': envVariables
        # };
        first_port = ContainerPort(container_port=22)
        ports = [first_port]
        first_container = Container(
            name="ubuntu-container", image="jupyter/minimal-notebook", ports=ports
        )
        # ubuntu:latest
        # jupyter/minimal-notebook
        containers = [first_container]
        pod_template = PodTemplate(containers=containers)
        deployment = Deployment(pod_template=pod_template)
        request = AuthWithDeployment(deployment=deployment)
        DC499999999EPME5000Consumer.create(request=request)
        return LaunchVMResponse()
