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

from ethos.elint.collars.DC499999999_caps_pb2 import (
    AuthWithDeployment,
    RepeatedDC499999999,
)
from ethos.elint.collars.DC499999999_caps_pb2_grpc import (
    DC499999999EPME5000CapabilitiesServicer,
)
from ethos.elint.collars.DC499999999_pb2 import (
    DC499999999,
    Condition,
    Deployment,
    DeploymentStatus,
)
from ethos.elint.entities.generic_pb2 import ResponseMeta
from kubernetes import client, config
from kubernetes.client import (
    V1Container,
    V1ContainerPort,
    V1Deployment,
    V1DeploymentSpec,
    V1LabelSelector,
    V1ObjectMeta,
    V1PodSpec,
    V1PodTemplateSpec,
    V1ResourceRequirements,
    V1Service,
    V1ServicePort,
    V1ServiceSpec,
    V1Ingress,
    V1IngressRule,
    V1HTTPIngressPath,
    V1IngressSpec,
    V1IngressBackend,
    V1IngressTLS,
)
from kubernetes.client.models.v1_service_backend_port import V1ServiceBackendPort

from src.community.gramx.collars.DC499999999.model import DC499999999Model
from src.community.gramx.fifty.zero.ethos.service_spaces.entities.space_service_domain.access.consumers.access_space_service_domain_consumer import (
    AccessSpaceServiceDomainConsumer,
)
from src.db_session import DbSession
from src.support.helper_functions import format_datetime_to_timestamp
from support.application.tracing import trace_rpc


def parsev1_deployment_proto(deployment_proto: Deployment) -> V1Deployment:
    # Validate essential fields
    if not deployment_proto.metadata:
        raise ValueError("Deployment metadata is missing.")
    if not deployment_proto.pod_template:
        raise ValueError("Pod template is missing.")
    if not deployment_proto.replica_config:
        raise ValueError("Replica configuration is missing.")
    if not deployment_proto.selector:
        raise ValueError("Selector is missing.")

    # Extract metadata
    metadata = deployment_proto.metadata
    replica_config = deployment_proto.replica_config
    pod_template = deployment_proto.pod_template

    # Parse containers
    containers = []
    for container_proto in pod_template.containers:
        logging.debug(f"Parsing container: {container_proto.name}")

        container_ports = [
            V1ContainerPort(container_port=port.container_port, protocol=port.protocol)
            for port in (container_proto.ports or [])
        ]

        resources = V1ResourceRequirements(
            limits={
                "cpu": getattr(container_proto.resource_limits, "cpu", "500m"),
                "memory": getattr(container_proto.resource_limits, "memory", "256Mi"),
            },
            requests={
                "cpu": getattr(container_proto.resource_requests, "cpu", "250m"),
                "memory": getattr(container_proto.resource_requests, "memory", "128Mi"),
            },
        )

        container = V1Container(
            name=container_proto.name,
            image=container_proto.image,
            ports=container_ports,
            resources=resources,
            command=container_proto.command or [],
            args=container_proto.args or [],
        )
        containers.append(container)

    container_proto = pod_template.containers[0]
    logging.info(
        f"parsev1_deployment_proto, command: {type(list(container_proto.command))}, {list(container_proto.command)}"
    )
    logging.info(
        f"parsev1_deployment_proto, args: {type(container_proto.args)}, {container_proto.args}"
    )

    container_ports = [
        V1ContainerPort(container_port=port.container_port, protocol=port.protocol)
        for port in (container_proto.ports or [])
    ]

    resources = V1ResourceRequirements(
        limits={
            "cpu": getattr(container_proto.resource_limits, "cpu", "500m"),
            "memory": getattr(container_proto.resource_limits, "memory", "256Mi"),
        },
        requests={
            "cpu": getattr(container_proto.resource_requests, "cpu", "250m"),
            "memory": getattr(container_proto.resource_requests, "memory", "128Mi"),
        },
    )

    # Define the container spec with Ubuntu and SSH setup
    container = V1Container(
        name=container_proto.name,
        image=container_proto.image,
        ports=container_ports,
        resources=resources,
        command=list(container_proto.command) or [],
        args=list(container_proto.args) or [],
    )

    containers = [container]

    # # Define the pod template
    template = V1PodTemplateSpec(
        metadata=V1ObjectMeta(
            labels=dict(pod_template.labels or {}),
            annotations=dict(pod_template.annotations or {}),
        ),
        spec=V1PodSpec(containers=containers),
    )

    logging.info(
        f"parsev1_deployment_proto, match_labels: {deployment_proto.selector.match_labels}"
    )
    logging.info(
        f"parsev1_deployment_proto, match_labels.2: {dict(deployment_proto.selector.match_labels or {})}"
    )

    # # Define the deployment spec
    deployment_spec = V1DeploymentSpec(
        replicas=replica_config.replicas or 1,
        selector=V1LabelSelector(
            match_labels=dict(deployment_proto.selector.match_labels or {})
        ),
        template=template,
    )

    # # Define the deployment
    deployment = V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=V1ObjectMeta(
            name=metadata.name or "default-name",
            namespace=metadata.namespace or "default",
            labels=dict(metadata.labels or {}),
            annotations=dict(metadata.annotations or {}),
        ),
        spec=deployment_spec,
    )

    logging.info(f"Successfully parsed deployment: {metadata.name}")
    return deployment


def parsev1_svc_from_deployment_proto(deployment_proto: Deployment) -> V1Service:
    # Extract metadata
    deployment_name = deployment_proto.metadata.name
    namespace = deployment_proto.metadata.namespace or "default"
    labels = dict(deployment_proto.metadata.labels) or {}

    # Determine ports from containerPorts
    ports = []
    for container in deployment_proto.pod_template.containers:
        for container_port in container.ports:
            ports.append(
                V1ServicePort(
                    port=container_port.container_port,  # Service port
                    target_port=container_port.container_port,  # Target port in the container
                    protocol=container_port.protocol or "TCP",  # Protocol
                )
            )

    if not ports:
        raise ValueError("No ports defined in container configuration for the service.")

    # Build the service object
    service = V1Service(
        api_version="v1",
        kind="Service",
        metadata=V1ObjectMeta(
            name=f"{deployment_name}-service",
            namespace=namespace,
            labels=labels,
        ),
        spec=V1ServiceSpec(
            selector=dict(deployment_proto.selector.match_labels or {}),
            ports=ports,
            type="NodePort",
        ),
    )
    return service


def create_ingress_for_https(deployment_proto: Deployment) -> V1Ingress:
    deployment_name = deployment_proto.metadata.name
    namespace = deployment_proto.metadata.namespace or "default"

    # Add annotations for certificate provisioning (e.g., Cert-Manager)
    annotations = {
        "kubernetes.io/ingress.class": "nginx",  # Adjust according to your Ingress Controller
        "cert-manager.io/cluster-issuer": "letsencrypt-prod",  # ClusterIssuer for Cert-Manager
    }

    # Define Ingress rule
    ingress_rule = V1IngressRule(
        host="",  # Remove {pod_name}.50gramx.com
        http=V1HTTPIngressPath(
            path="/",
            path_type="Prefix",
            backend=V1IngressBackend(
                service=V1ServiceBackendPort(
                    name=f"{deployment_name}-service",  # Service reference
                    port=V1ServiceBackendPort(port=443),  # Map to HTTPS port
                )
            ),
        ),
    )

    # Define Ingress TLS
    ingress_tls = V1IngressTLS(
        hosts=[],  # No hostname required
        secret_name=f"{deployment_name}-tls-secret",
    )

    # Create the Ingress object
    ingress = V1Ingress(
        api_version="networking.k8s.io/v1",
        kind="Ingress",
        metadata=V1ObjectMeta(
            name=f"{deployment_name}-ingress",
            namespace=namespace,
            annotations=annotations,
        ),
        spec=V1IngressSpec(rules=[ingress_rule], tls=[ingress_tls]),
    )

    return ingress


class DC499999999EPME5000Capabilities(DC499999999EPME5000CapabilitiesServicer):
    def __init__(self):
        super(DC499999999EPME5000Capabilities, self).__init__()
        self.session_scope = self.__class__.__name__
        self.ccode = "DC499999999"
        #  Load the Kubernetes configuration
        config.load_kube_config(
            config_file="/app/src/community/gramx/collars/DC499999999/microk8s-config"
        )  # This assumes you have a kubeconfig file set up

    @trace_rpc()
    def Create(self, request, context):
        logging.info(f"{self.session_scope}:Create")
        logging.info(f"{self.session_scope}:Create: request: {request}")

        # objective: add the deployment to the database
        # load the db
        cmodel = DC499999999Model(
            space_service_domain_id=request.auth.space_service_domain.id,
            space_service_domain_collar_code=self.ccode,
        )
        # insert deployment
        did = cmodel.add_deployment_from_proto(deployment_proto=request.deployment)
        # insert collar
        cid = cmodel.add_collar(deployment_id=did)
        # insert label selectors
        saved_c = cmodel.get_collar(id=cid)

        # Extract the existing labels from the proto
        existing_labels = saved_c.deployment.metadata.labels
        existing_match_labels = saved_c.deployment.selector.match_labels
        existing_template_labels = saved_c.deployment.pod_template.labels

        # Update the labels with new key-value pairs
        new_labels = {
            "collar_id": cid,
            "deployment_id": did,
            "domain_id": request.auth.space_service_domain.id,
        }

        # Update or add new key-value pairs
        for key, value in new_labels.items():
            existing_labels[key] = value
            existing_match_labels[key] = value
            existing_template_labels[key] = value

        # Saving the metadata
        cmodel.update_metadata_labels_from_proto(saved_c.deployment.metadata)

        # second run the deployment
        deployment = parsev1_deployment_proto(saved_c.deployment)
        logging.info(f"Deployment parsed. deployment='{deployment}'")

        apps_v1 = client.AppsV1Api()
        deployment_response = apps_v1.create_namespaced_deployment(
            body=deployment,
            namespace="default",  # Use the appropriate namespace
        )
        logging.info(
            f"Deployment created. Status='{deployment_response.metadata.name}'"
        )
        logging.info(f"Deployment created. Response='{deployment_response}'")

        # third fetch the current state and update parameters for needed intel

        # Create the deployment

        # Define a service to expose the SSH port on a NodePort
        service = parsev1_svc_from_deployment_proto(saved_c.deployment)

        # Create the service (ClusterIP)
        core_v1 = client.CoreV1Api()
        service_response = core_v1.create_namespaced_service(
            namespace="default", body=service
        )

        logging.info(
            f"Service created. Name='{service_response.metadata.name}', NodePort={service_response.spec.ports[0].node_port}"
        )

        # Create the Ingress for HTTPS
        ingress = create_ingress_for_https(saved_c.deployment)

        # Create the ingress resource
        networking_v1 = client.NetworkingV1Api()
        ingress_response = networking_v1.create_namespaced_ingress(
            namespace="default", body=ingress
        )

        logging.info(f"Ingress created. Name='{ingress_response.metadata.name}'")

        return AuthWithDeployment()

    @trace_rpc()
    def List(self, request, context):
        logging.info(f"{self.session_scope}:List")
        done, msg = (
            AccessSpaceServiceDomainConsumer.validate_space_service_domain_services(
                request
            )
        )
        meta = ResponseMeta(meta_done=done, meta_message=msg)
        if done is False:
            return meta
        else:
            # load the db
            cmodel = DC499999999Model(
                space_service_domain_id=request.space_service_domain.id,
                space_service_domain_collar_code=self.ccode,
            )
            # get list of collars
            cs = cmodel.get_collar_all()
            return RepeatedDC499999999(collars=cs, meta=meta)

    @trace_rpc()
    def Get(self, request, context):
        logging.info(f"{self.session_scope}:Get")
        done, msg = (
            AccessSpaceServiceDomainConsumer.validate_space_service_domain_services(
                request.auth
            )
        )
        meta = ResponseMeta(meta_done=done, meta_message=msg)
        if done is False:
            return Deployment()
        else:
            # load the db
            cmodel = DC499999999Model(
                space_service_domain_id=request.auth.space_service_domain.id,
                space_service_domain_collar_code=self.ccode,
            )
            # get list of collars
            c = cmodel.get_collar(id=request.collar_id)

            # List deployments with a label selector
            selectors = {
                "collar_id": f"{request.collar_id}",
                "deployment_id": f"{c.deployment.id}",
                "domain_id": f"{request.auth.space_service_domain.id}",
            }
            label_selector = ",".join(
                [f"{key}={value}" for key, value in selectors.items()]
            )

            logging.info(f"Deployment List. selectors='{selectors}'")
            apps_v1 = client.AppsV1Api()
            deployments = apps_v1.list_namespaced_deployment(
                namespace="default", label_selector=label_selector, timeout_seconds=56
            )
            logging.info(f"Deployment List. Details='{deployments}'")
            core_v1 = client.CoreV1Api()
            services = core_v1.list_namespaced_service(
                namespace="default", label_selector=label_selector, timeout_seconds=56
            )
            logging.info(f"Service List. Details='{services}'")

            node_ports = []
            for service in services.items:
                # Access the ports from the service's spec
                ports = getattr(service.spec, "ports", [])
                for port in ports:
                    node_port = getattr(port, "node_port", None)
                    target_port = getattr(port, "target_port", None)
                    if node_port is not None and target_port is not None:
                        node_ports.append(
                            {"node_port": node_port, "target_port": target_port}
                        )

            logging.info(f"Service List. NodePorts='{node_ports}'")

            matched_port = None
            for container in c.deployment.pod_template.containers:
                for port in container.ports:
                    # Match container_port with target_port in node_ports
                    matching_node_port = next(
                        (
                            np["node_port"]
                            for np in node_ports
                            if np["target_port"] == port.container_port
                        ),
                        None,
                    )
                    # If a match is found, set the node_port
                    if matching_node_port is not None:
                        matched_port = matching_node_port
                        port.node_port = matched_port
            logging.info(f"Service List. NodePort='{matched_port}'")

            for deployment in deployments.items:
                deployment_status = deployment.status
                # Create DeploymentStatus protobuf instance
                status_proto = DeploymentStatus(
                    id=deployment.metadata.uid,
                    deployment_id=deployment.metadata.name,
                    replicas=deployment_status.replicas or 0,
                    updated_replicas=deployment_status.updated_replicas or 0,
                    available_replicas=deployment_status.available_replicas or 0,
                    unavailable_replicas=deployment_status.unavailable_replicas or 0,
                )

                # Process conditions
                for cond in deployment_status.conditions or []:
                    logging.info(
                        f"last_update_time={cond.last_update_time}, type={type(cond.last_update_time)}"
                    )
                    logging.info(
                        f"last_update_time={cond.last_transition_time}, type={type(cond.last_transition_time)}"
                    )
                    condition_proto = Condition(
                        type=cond.type,
                        status=cond.status,
                        reason=cond.reason,
                        message=cond.message,
                        last_update_time=format_datetime_to_timestamp(
                            cond.last_update_time
                        ),
                        last_transition_time=format_datetime_to_timestamp(
                            cond.last_transition_time
                        ),
                    )
                    status_proto.conditions.append(condition_proto)

                # Log or process the populated DeploymentStatus
                logging.info(f"Deployment Status Proto: {status_proto}")
                c.deployment.status.CopyFrom(status_proto)

            return c.deployment
