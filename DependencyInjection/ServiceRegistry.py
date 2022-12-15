class ServiceRegistry:
    services_container: Dict[str, ] = {}

    def get_name_of_type(self, value: type):
        print(value.__name__)