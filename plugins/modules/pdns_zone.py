#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: pdns_zone
short_description: Manage DNS zones on PowerDNS authoritative server
description:
  - Manage DNS zones on PowerDNS authoritative server
author: Rytis Sileika (@rytis)
requirements:
  - requests
options:
  - state:
      description:
        - Zone state
      type: str
      choices: [present, absent]
      required: True
  - api_url:
      description:
        - PowerDNS authoritative server API URL
      type: str
      required: True
  - api_token:
      description:
        - API token
      type: str
      required: True
  - name:
      description:
        - Name of the zone to manage
      type: str
      required: True
"""

EXAMPLES = """
    - name: Create new zone record
      rytis.utils.pdns_zone:
        api_url: "http://pdns_auth_server_fqdn:8081/"
        api_token: "<secret_auth_token>"
        name: "example.com"
        state: "present"
"""


import requests
from ansible.module_utils.basic import AnsibleModule


class PDNSAuthClient:
    """Client class to interact with PowerDNS authoritative server

    :param url: URL of PowerDNS Auth API service
    :param auth_key: Auth key to allow access to the API service
    :param server: server name to manage. Default: `localhost`
    """

    def __init__(self, url, auth_key, server="localhost"):
        self.server_base_url = "{}/api/v1/servers/{}".format(url, server)
        self.zones_url = "{}/zones".format(self.server_base_url)
        self.auth_header = {"X-API-Key": auth_key}

    def create_zone(self, zone):
        """Create new zone if the zone does not exist yet

        :param zone: Name of the zone to create. Must include trailing period
        :returns: `True` if the zone was created, `False` if the zone already exists.
        """

        if self._zone_exists(zone):
            return False
        zone_data = {
            "name": zone,
            "type": "Zone",
            "kind": "Master",
            "nameservers": ["ns.{}".format(zone),],
        }
        r = requests.post(self.zones_url, headers=self.auth_header, json=zone_data)
        return True

    def delete_zone(self, zone):
        """Remove zone if it exists

        :param zone: Name of the zone to remove.
        :returns: `True` if the zone was removed, `False` if the zone does not exist.
        """

        if not self._zone_exists(zone):
            return False
        zone_url = "{}/{}".format(self.zones_url, zone)
        r = requests.delete(zone_url, headers=self.auth_header)
        return True

    def _zone_exists(self, zone):
        """Check if the zone exists"""

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

