from ethos.elint.collars.DC499999994_caps_pb2_grpc import (
    DC499999994EPME5000CapabilitiesStub,
)

from support.application.registry import Registry


def load_DC499999994_stubs(capabilities_common_channel):
    dc499999994_epme5000_capabilities_stub = DC499999994EPME5000CapabilitiesStub(
        capabilities_common_channel
    )
    Registry.register_service(
        "dc499999994_epme5000_capabilities_stub",
        dc499999994_epme5000_capabilities_stub,
    )
