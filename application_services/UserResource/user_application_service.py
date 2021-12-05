from framework.base_application_resource import BaseApplicationResource

class UserResource(BaseApplicationResource):

    def __init__(self, config_info):
        super().__init__(config_info)

    def get_links(self, resource_data):
        for r in resource_data:
            user_id = r.get('id')

            links = []
            self_link = {"rel": "self", "href": "/api/user/" + str(user_id)}
            links.append(self_link)

            r["links"] = links

        return resource_data

    def create(self, new_resource_info):
        db_svc = self._get_db_resource()
        if "email" not in new_resource_info or "phone" not in new_resource_info or "name" not in new_resource_info:
            return -1
        next_id = db_svc.get_next_id()
        new_resource_info["id"] = next_id
        res = super().create(new_resource_info)

        if res == 1:
            res = {}
            res["location"] = "/api/user/" + str(next_id)

        return res
