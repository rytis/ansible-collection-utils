#!/usr/bin/python
# -*- coding: utf-8 -*-


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

