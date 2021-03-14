#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule


class DnsClient():
    def __init__(self):
        pass


def main():
    module = AnsibleModule(
        argument_spec={}
    )
    dns_client = DnsClient()
    module.exit_json()


if __name__ == "__main__":
    main()

