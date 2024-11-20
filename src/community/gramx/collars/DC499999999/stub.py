from ethos.elint.collars.DC499999999_caps_pb2_grpc import (
    DC499999999EPME5000CapabilitiesStub,
)

from support.application.registry import Registry


def load_DC499999999_stubs(capabilities_common_channel):
    dc499999999_epme5000_capabilities_stub = DC499999999EPME5000CapabilitiesStub(
        capabilities_common_channel
    )
    Registry.register_service(
        "dc499999999_epme5000_capabilities_stub",
        dc499999999_epme5000_capabilities_stub,
    )
