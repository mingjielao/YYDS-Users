from application_services.BaseApplicationResource import BaseRDBApplicationResource
from database_services.RDBService import RDBService


class UserResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        for r in resource_data:
            address_id = r.get('addressID')
            user_id = r.get('ID')

            links = []
            self_link = {"rel": "self", "href": "/users/" + str(user_id)}
            links.append(self_link)

            if address_id is not None:
                address_link = {"rel": "address", "href": "/address/" + str(address_id)}
                links.append(address_link)

            r["links"] = links

        return resource_data


    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'users'

    @classmethod
    def get_by_name_prefix(cls, name_prefix):
        res = RDBService.get_by_prefix("aaaaaF21E6156", "users",
                                      "name", name_prefix)
        return res

    @classmethod
    def get_by_template(cls):
        res = RDBService.find_by_template("aaaaaF21E6156", "users",
                                       )
        return res


    @classmethod
    def get_by_name_userid(cls, name_userid):
        res = RDBService.get_by_userid("EventShare_UserAddress", "User",
                                      "ID", name_userid)
        return res


    @classmethod
    def get_next_id(cls, table_name):
        res = RDBService.get_next_id("EventShare_UserAddress", table_name)
        return res

    @classmethod
    def create(cls, table_name, data):
        res = RDBService.create("EventShare_UserAddress", table_name, data)
        return res