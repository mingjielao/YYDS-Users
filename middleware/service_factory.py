import middleware.context as context

from application_services.UserResource.user_application_service import UserResource
from database_services.user_rdb_service import UserRDBService

class ServiceFactory:

    def __init__(self):
        self.db_connect_info = context.get_db_info()
        e_svc = UserRDBService(self.db_connect_info)

        self.services = {}

        event_svc_config_info = {
            "db_resource": e_svc,
            "db_table_name": "user",
            "key_columns": ["id"]
        }
        event_svc = UserResource(event_svc_config_info)

        self.services["user"] = event_svc

    def get_service(self, service_name):
        result = self.services.get(service_name, None)
        return result
