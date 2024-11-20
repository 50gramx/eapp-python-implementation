from ethos.elint.collars.DC499999998_pb2_grpc import DC499999998EPME5000CapabilitiesStub

from support.application.registry import Registry


def load_DC499999998_stubs(capabilities_common_channel):
    dc499999998_epme5000_capabilities_stub = DC499999998EPME5000CapabilitiesStub(
        capabilities_common_channel
    )
    Registry.register_service(
        "dc499999998_epme5000_capabilities_stub",
        dc499999998_epme5000_capabilities_stub,
    )
