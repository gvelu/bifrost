#!/usr/bin/env python
# coding: utf-8 -*-

# (c) 2015, Hewlett-Packard Development Company, L.P.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: network_metadata
short_description: Returns a config-drive network-metadata dictionary
extends_documentation_fragment: openstack
'''


def main():
    argument_spec = dict(
        ipv4_address=dict(required=False),
        ipv4_gateway=dict(required=False),
        ipv4_interface_mac=dict(required=False),
        ipv4_nameserver=dict(required=False),
        ipv4_subnet_mask=dict(required=False),
        network_mtu=dict(required=False),
        nics=dict(required=False),
        node_network_info=dict(required=False)
    )

    module = AnsibleModule(argument_spec)

    network_metadata = module.params['node_network_info']
    if not network_metadata:
        links = []
        networks = []

        if module.params['ipv4_interface_mac']:
            links.append({
                'id': module.params['ipv4_interface_mac'],
                'type': 'phy',
                'ethernet_mac_address': module.params['ipv4_interface_mac'],
                'mtu': module.params['network_mtu']
            })

            for nic in module.params['nics']:
                if nic['mac'] == module.params['ipv4_interface_mac']:
                    networks.append({
                        'id': 'ipv4-%s' % nic['mac'],
                        'link': nic['mac'],
                        'type': 'ipv4',
                        'ip_address': module.params['ipv4_address'],
                        'netmask': module.params['ipv4_subnet_mask'],
                        'dns_nameservers': [
                            module.params['ipv4_nameserver']
                        ],
                        'routes': [{
                            'network': '0.0.0.0',
                            'netmask': '0.0.0.0',
                            'gateway': module.params['ipv4_gateway']
                        }]
                    })
        else:
            for i, nic in enumerate(module.params['nics']):
                links.append({
                    'id': nic['mac'],
                    'type': 'phy',
                    'ethernet_mac_address': nic['mac'],
                    'mtu': module.params['network_mtu']
                })

                if i == 0:
                    networks.append({
                        'id': 'ipv4-%s' % nic['mac'],
                        'link': nic['mac'],
                        'type': 'ipv4',
                        'ip_address': module.params['ipv4_address'],
                        'netmask': module.params['ipv4_subnet_mask'],
                        'dns_nameservers': [
                            module.params['ipv4_nameserver']
                        ],
                        'routes': [{
                            'network': '0.0.0.0',
                            'netmask': '0.0.0.0',
                            'gateway': module.params['ipv4_gateway']
                        }]
                    })
                else:
                    networks.append({
                        'id': 'ipv4-dhcp-%s' % nic['mac'],
                        'link': nic['mac'],
                        'type': 'ipv4_dhcp',
                    })

        network_metadata = {
            'links': links,
            'networks': networks
        }
        facts = {'network_metadata': network_metadata}

        module.exit_json(changed=False, ansible_facts=facts)


# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
