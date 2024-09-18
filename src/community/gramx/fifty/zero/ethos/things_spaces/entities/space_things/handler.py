import logging

from ethos.elint.services.product.identity.space_things.create_space_things_pb2_grpc import \
    add_CreateServiceServicer_to_server


from application_context import ApplicationContext


def handle_space_knowledge_services(server, aio: bool):
    if aio:
        pass
    else:
        add_CreateServiceServicer_to_server(
            ApplicationContext.get_create_space_things_domain_service(), server
        )
        logging.info(f'\t\t [x] create')