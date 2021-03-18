#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from ansible.module_utils.basic import AnsibleModule


class PDNSAuthClient:
    def __init__(self, url, auth_key, server="localhost"):
        self.server_base_url = "{}/api/v1/servers/{}".format(url, server)
        self.zones_url = "{}/zones".format(self.server_base_url)
        self.auth_header = {"X-API-Key": auth_key}

    def create_zone(self, zone):
        if self._zone_exists(zone):
            return False
        zone_data = {
            "name": zone,
            "type": "Zone",
            "kind": "Master",
        }
        r = requests.post(self.zones_url, headers=self.auth_header, json=zone_data)
        return True

    def delete_zone(self, zone):
        if not self._zone_exists(zone):
            return False
        zone_url = "{}/{}".format(self.zones_url, zone)
        r = requests.delete(zone_url, headers=self.auth_header)
        return True

    def _zone_exists(self, zone):
        r = requests.get(self.zones_url, headers=self.auth_header, params={"zone": zone})
        return 0 < len(r.json())


def main():
    module = AnsibleModule(
        argument_spec={
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "api_url": {"type": "str", "required": True},
            "api_token": {"type": "str", "required": True},
            "name": {"type": "str", "required": True},
        }
    )

    c = PDNSAuthClient(module.params["api_url"], module.params["api_token"])
    changed = False

    if module.params["state"] == "present":
        changed = c.create_zone(module.params["name"])
    elif module.params["state"] == "absent":
        changed = c.delete_zone(module.params["name"])

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()

