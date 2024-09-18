from community.gramx.fifty.zero.ethos.things_spaces.entities.space_things.create.capabilities.create_space_things_service import CreateSpaceThingsService
from support.application.registry import Registry



def register_space_knowledge_domain_services(aio: bool):
    if aio:
        pass
    else:
        create_space_things_domain_service = CreateSpaceThingsService()
        Registry.register_service('create_Space_things_domain_service', create_space_things_domain_service)