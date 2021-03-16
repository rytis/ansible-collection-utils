#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
module: dns_client
short_description: Manage DNS records on various DNS providers
description:
  - Manage DNS records on a selection of popular DNS providers.
    Module uses `python-lexicon` under the hood to interact with
    DNS providers
author: Rytis Sileika (@rytis)
requirements:
  - python-lexicon
options:
  - provider_name:
      description:
        - Name of the provider to use. Must match a name of the available providers in `python-lexicon`
      type: str
      required: True
  - action:
      description:
        - Action to perform
      type: str
      choices: [create, delete]
      required: True
  - domain:
      description:
        - Top level domain name
      type: str
      required: True
  - type:
      description:
        - Type of record to manage
      type: str
      choices: [A, AAAA, CNAME, MX, NS, SOA, TXT, SRV]
  - name:
      description:
        - Name of the entry
      type: str
  - content:
      description:
        - Contents of the record. The actual contents
          depend on the record type. For an A record this
          would be an IP address.
      type: str
  - delegated:
      description:
        - If records are te be managed for a subdomain, this
          specifies subdomain name
      type: str
  - provider_options:
      description:
        - Provider specific options, such as server URI and
          authentication details
      type: dict
      required: True
"""

from ansible.module_utils.basic import AnsibleModule
from lexicon.client import Client
from lexicon.config import ConfigResolver


SUPPORTED_RECORDS = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT", "SRV"]


def main():
    module = AnsibleModule(
        argument_spec={
            "provider_name": {"type": "str", "required": True},
            "action": {"type": "str", "required": True},
            "domain": {"type": "str", "required": True},
            "type": {"type": "str", "choices": SUPPORTED_RECORDS},
            "name": {"type": "str"},
            "content": {"type": "str"},
            "delegated": {"type": "str", "default": None},
            "provider_options": {"type": "dict", "required": True},
        }
    )
    action = {
        "provider_name": module.params["provider_name"],
        "action": module.params["action"],
        "delegated": module.params["delegated"],
        "domain": module.params["domain"],
        "type": module.params["type"],
        "name": module.params["name"],
        "content": module.params["content"],
        module.params["provider_name"]: module.params["provider_options"],
    }
    config = ConfigResolver().with_dict(action)
    Client(config).execute()
    module.exit_json()


if __name__ == "__main__":
    main()

