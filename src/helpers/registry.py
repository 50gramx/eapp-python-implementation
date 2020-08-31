class Registry(object):
    __services = dict()
    __data = dict()


    @staticmethod
    def register_service(name: str, service: object):
        if name in Registry.__services:
            raise RuntimeError('Service with name {0} already registered!'.format(name))

        Registry.__services[name] = service

    @staticmethod
    def get_service(name: object) -> object:
        if name in Registry.__services:
            return Registry.__services.get(name)
        return None

    @staticmethod
    def register_data(name: str, value: object):
        Registry.__data[name] = value

    @staticmethod
    def get_data(name: object) -> object:
        return Registry.__data.get(name)

    @staticmethod
    def delete_data(name: object) -> bool:
        if Registry.__data.get(name, False):
            Registry.__data.pop(name)
            return True
        else:
            return False