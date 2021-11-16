#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: design

short_description: Manage Design elements within Apstra.

version_added: "0.0.1"

description: This module will leverage Apstra's REST API to automate the management of Design elements within Apstra.

options:
    api_token:
        description:
          - used to authenticate to the API
        required: true
        type: str
    device_profile_id:
        description:
            - the name you would like to associate to the interface mapping goes here
        required: true
        type: str
    display_name:
        description:
            - the name you would like to associate to these networks goes here
        required: true
        type: str
    interfaces:
        description:
          - interfaces mapped out
        required: false
        type: list
    label:
        description:
          - label name
        required: false
        type: str
    logical_device_id:
        description:
          - logical_device_id name
        required: false
        type: str
    name:
        required=False,
        type='str'
    panels:
        required=False,
        type='list'
    port:
        description:
            - port number (integer) used by the Apstra AIS server
            - defaults to 443
        required: true
        type: int
    server:
        description:
            - DNS hostname or IP address of your Apstra AIS server
            - can leverage an environment of MIST_ORG_ID on your Ansible host
        required: true
        type: str
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str
    type:
        description:
            - specify which type of resource you would like to manage
        required: true
        choices:
          - 'logical-devices'
          - 'interface-maps'
        type: str
    validate_certs:
        description:
            - whether or not the certificate is valid
            - may help those behind proxies
        required: false
        default: true
        type: bool

extends_documentation_fragment:
    - cremsburg.apstra.design

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
---
### #################################################################
### # CREATE RESOURCES PLAY
### #################################################################
- hosts: localhost
  gather_facts: False
  become: False
  tasks:
    ### #################################################################
    ### # AUTHENTICATE AND RECEIVE AN API TOKEN FROM THE APSTRA SERVER
    ### #################################################################
    - name: retrieve an API token for our session
      ansible.builtin.uri:
        url: https://apstra.dmz.home/api/user/login
        method: POST
        headers:
          Content-Type: application/json
        status_code: 201
        validate_certs: False
        body_format: json
        body:
          username: apstra
          password: apstra123
      register: api_token

    - name: create 'api_token' object by setting it equal to value in response
      ansible.builtin.set_fact:
        api_token: "{{ api_token.json.token }}"

    ### #################################################################
    ### # CREATE IP POOL RESOURCES
    ### #################################################################
    - name: "### CREATE IP POOL cicd_leaf_loopbacks"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_leaf_loopbacks"
        type: "ip-pools"
        tags:
          - cicd
          - leaf
        subnets:
          - "10.255.2.0/24"

        # define to delete or create
        state: present

    - name: "### CREATE IP POOL cicd_spine_loopbacks"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_spine_loopbacks"
        type: "ip-pools"
        tags:
          - cicd
          - spine
        subnets:
          - "10.255.1.0/24"

        # define to delete or create
        state: present

    - name: "### CREATE IP POOL cicd_fabric_underlay"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_fabric_underlay"
        type: "ip-pools"
        tags:
          - cicd
          - fabric
        subnets:
          - "172.20.1.0/24"

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE ASN POOL RESOURCES
    ### #################################################################
    - name: "### CREATE ASN POOL cicd_asn_pool"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "asn-pools"
        display_name: "cicd_asn_pool"
        tags:
          - cicd
        ranges:
          - first: 65010
            last: 65019
          - first: 65110
            last: 65119

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE VNI POOL RESOURCES
    ### #################################################################
    - name: "### CREATE VNI POOL cicd_vni_pool"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "vni-pools"
        display_name: "cicd_vni_pool"
        tags:
          - cicd
        ranges:
          - first: 10000
            last: 19999
          - first: 100000
            last: 109999

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE VLAN POOL RESOURCES
    ### #################################################################
    - name: "### CREATE VLAN POOL cicd_vlan_pool"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_vlan_pool"
        type: "vlan-pools"
        tags:
          - cicd
        ranges:
          - first: 100
            last: 199
          - first: 1000
            last: 1999

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE EXTERNAL ROUTER RESOURCE
    ### #################################################################
    - name: "### CREATE EXTERNAL ROUTER cicd_external_router"
      cremsburg.apstra.resources:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        display_name: "cicd_external_router"
        address: "192.168.10.255"
        ipv6_address: "fc01:a05:192:168:10::255"
        asn: 65000
        type: "external-routers"

        # define to delete or create
        state: present

### #################################################################
### # CREATE DESIGN PLAY
### #################################################################
- hosts: localhost
  gather_facts: False
  become: False
  tasks:
    ### #################################################################
    ### # AUTHENTICATE AND RECEIVE AN API TOKEN FROM THE APSTRA SERVER
    ### #################################################################
    - name: retrieve an API token for our session
      ansible.builtin.uri:
        url: https://apstra.dmz.home/api/user/login
        method: POST
        headers:
          Content-Type: application/json
        status_code: 201
        validate_certs: False
        body_format: json
        body:
          username: apstra
          password: apstra123
      register: api_token

    - name: create 'api_token' object by setting it equal to value in response
      ansible.builtin.set_fact:
        api_token: "{{ api_token.json.token }}"

    ### #################################################################
    ### # CREATE NEW LOGICAL DEVICES FOR SPINE AND LEAF
    ### #################################################################
    - name: "### CREATE LOGICAL DEVICE cicd_spine"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "logical-devices"
        display_name: "cicd_spine"
        panels:
          - panel_layout:
              row_count: 1
              column_count: 12
            port_indexing:
              order: "T-B, L-R"
              schema: "absolute"
              start_index: 1
            port_groups:

              # ports xe-0/0/0-11, connections to leafs
              - count: 12
                roles:
                  - leaf
                speed:
                  value: 10
                  unit: "G"

        # define to delete or create
        state: present
      register: logical_device_cicd_spine

    - name: "### CREATE LOGICAL DEVICE cicd_leaf"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "logical-devices"
        display_name: "cicd_leaf"
        panels:
          - panel_layout:
              row_count: 1
              column_count: 12
            port_indexing:
              order: "T-B, L-R"
              schema: "absolute"
              start_index: 1
            port_groups:
              # ports xe-0/0/0-3, connections to spine
              - count: 4
                roles:
                  - spine
                speed:
                  value: 10
                  unit: "G"
              # ports xe-0/0/4-10, connections to servers
              - count: 7
                roles:
                  - l2_server
                  - l3_server
                  - access
                speed:
                  value: 10
                  unit: "G"
              # port xe-0/0/11, connections to external router
              - count: 1
                roles:
                  - external_router
                speed:
                  value: 10
                  unit: "G"

        # define to delete or create
        state: present
      register: logical_device_cicd_leaf

    ### #################################################################
    ### # CREATE A NEW INTERFACE MAPPING
    ### #################################################################
    - name: "### CREATE INTERFACE MAPPING cicd_spine"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "interface-maps"
        label: "cicd_spine_interface_mapping"
        logical_device_id: "{{ logical_device_cicd_spine['data']['id'] }}"
        device_profile_id: "Juniper_vQFX"
        interfaces: "{{ interface_map_vqfx_spine }}"

        # define to delete or create
        state: present

    - name: "### CREATE INTERFACE MAPPING cicd_leaf"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "interface-maps"
        label: "cicd_leaf_interface_mapping"
        logical_device_id: "{{ logical_device_cicd_leaf['data']['id'] }}"
        device_profile_id: "Juniper_vQFX"
        interfaces: "{{ interface_map_vqfx_leaf }}"

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE A NEW RACK TYPE
    ### #################################################################
    - name: "### CREATE RACK TYPE cicd_rack"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "rack-types"
        label: "cicd_rack"
        access_switches: []
        description: cicd_rack
        display_name: cicd_rack
        id: cicd_rack
        leafs:
          - link_per_spine_count: 1
            redundancy_protocol:
            leaf_leaf_link_speed:
            external_router_links: []
            leaf_leaf_l3_link_count: 0
            leaf_leaf_l3_link_speed:
            link_per_spine_speed:
              unit: G
              value: 10
            external_router_facing: false
            label: cicd_leaf
            leaf_leaf_l3_link_port_channel_id: 0
            leaf_leaf_link_port_channel_id: 0
            logical_device: "{{ logical_device_cicd_leaf['data']['id'] }}"
            leaf_leaf_link_count: 0
        logical_devices:
          - display_name: AOS-1x10-1
            id: AOS-1x10-1
            panels:
              - panel_layout:
                  row_count: 1
                  column_count: 1
                port_indexing:
                  order: T-B, L-R
                  start_index: 1
                  schema: absolute
                port_groups:
                  - count: 1
                    speed:
                      unit: G
                      value: 10
                    roles:
                      - leaf
                      - access
          - display_name: cicd_leaf
            id: "{{ logical_device_cicd_leaf['data']['id'] }}"
            panels:
              - panel_layout:
                  row_count: 1
                  column_count: 12
                port_indexing:
                  order: T-B, L-R
                  start_index: 1
                  schema: absolute
                port_groups:
                  - count: 4
                    speed:
                      unit: G
                      value: 10
                    roles:
                      - spine
                  - count: 7
                    speed:
                      unit: G
                      value: 10
                    roles:
                      - l2_server
                      - access
                      - l3_server
                  - count: 1
                    speed:
                      unit: G
                      value: 10
                    roles:
                      - external_router
        servers:
          - count: 1
            ip_version: ipv4
            port_channel_id_min: 0
            port_channel_id_max: 0
            connectivity_type: l2
            links:
              - link_per_switch_count: 1
                link_speed:
                  unit: G
                  value: 10
                target_switch_label: cicd_leaf
                lag_mode:
                leaf_peer:
                attachment_type: singleAttached
                label: cicd_leaf_server
            label: cicd_server
            logical_device: AOS-1x10-1

        # define to delete or create
        state: present

    ### #################################################################
    ### # CREATE A TEMPLATE
    ### #################################################################
    - name: "### CREATE TEMPLATE cicd_template"
      cremsburg.apstra.design:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        type: "templates"
        design_template: "{{ cicd_template }}"

        # define to delete or create
        state: present
      register: templates

    # - name: debug templates to screen
    #   debug:
    #     msg: "{{ templates }}"

'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.apstra.plugins.module_utils.apstra.api import ApstraHelper
from ansible.module_utils._text import to_native


def rack_types(resources, module, rest):
    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    design_element = dict()
    design_element['id'] = None
    design_element['provisioned'] = False
    for each in resources["items"]:
        if each['id'] == module.params['id']:
            design_element['id'] = each['id']
            design_element['provisioned'] = True
    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if design_element['provisioned'] is True:
            response = rest.delete(f"design/rack-types/{design_element['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="Rack Type does not exist, exiting")

    # #######################################################################
    # looking to either create or update a Rack Type
    # #######################################################################
    else:

        # #######################################################################
        # create the Rack Type if it doesn't already exist
        # #######################################################################
        if design_element['provisioned'] is False:

            # ###########################################################################
            # design_element_data: parameters entered by the user to create the resource
            # ###########################################################################
            design_element_data = dict(access_switches=module.params['access_switches'],
                                       description=module.params['description'],
                                       display_name=module.params['display_name'],
                                       id=module.params['id'],
                                       leafs=module.params['leafs'],
                                       logical_devices=module.params['logical_devices'],
                                       servers=module.params['servers'])

            response = rest.post(f"design/rack-types", data=design_element_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=design_element)


def interface_maps(resources, module, rest):
    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    design_element = dict()
    design_element['id'] = None
    design_element['label'] = None
    design_element['provisioned'] = False
    for each in resources["items"]:
        if each['label'] == module.params['label']:
            design_element['id'] = each['id']
            design_element['label'] = each['label']
            design_element['provisioned'] = True
    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if design_element['provisioned'] is True:
            response = rest.delete(f"design/interface-maps/{design_element['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="Interface Mapping does not exist, exiting")

    # #######################################################################
    # looking to either create or update a interface mapping
    # #######################################################################
    else:

        # #######################################################################
        # create the interface mapping if it doesn't already exist
        # #######################################################################
        if design_element['provisioned'] is False:

            # ###########################################################################
            # design_element_data: parameters entered by the user to create the resource
            # ###########################################################################
            design_element_data = dict(device_profile_id=module.params['device_profile_id'],
                                       logical_device_id=module.params['logical_device_id'],
                                       interfaces=module.params['interfaces'],
                                       label=module.params['label'])

            response = rest.post(f"design/interface-maps", data=design_element_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=design_element)


def logical_device(resources, module, rest):
    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    design_element = dict()
    design_element['display_name'] = None
    design_element['id'] = None
    design_element['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            design_element['display_name'] = each['display_name']
            design_element['id'] = each['id']
            design_element['provisioned'] = True
    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if design_element['provisioned'] is True:
            response = rest.delete(f"design/logical-devices/{design_element['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="Logical Device does not exist, exiting")

    # #######################################################################
    # looking to either create or update a logical device
    # #######################################################################
    else:

        # #######################################################################
        # create the logical device if it doesn't already exist
        # #######################################################################
        if design_element['provisioned'] is False:

            # ###########################################################################
            # design_element_data: parameters entered by the user to create the resource
            # ###########################################################################
            design_element_data = dict(display_name=module.params['display_name'],
                                       panels=module.params['panels'])

            response = rest.post(f"design/logical-devices", data=design_element_data)
            design_element_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=design_element)


def templates(resources, module, rest):
    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    design_element = dict()
    design_element['display_name'] = None
    design_element['id'] = None
    design_element['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['design_template']['display_name']:
            design_element['display_name'] = each['display_name']
            design_element['id'] = each['id']
            design_element['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if design_element['provisioned'] is True:
            response = rest.delete(f"design/templates/{design_element['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="Template does not exist, exiting")

    # #######################################################################
    # looking to either create or update a logical device
    # #######################################################################
    else:

        # #######################################################################
        # create the logical device if it doesn't already exist
        # #######################################################################
        if design_element['provisioned'] is False:

            # ###########################################################################
            # design_element_data: parameters entered by the user to create the resource
            # ###########################################################################
            design_element_data = dict(
                                        asn_allocation_policy=module.params['design_template']['asn_allocation_policy'],
                                        dhcp_service_intent=module.params['design_template']['dhcp_service_intent'],
                                        display_name=module.params['design_template']['display_name'],
                                        external_routing_policy=module.params['design_template']['external_routing_policy'],
                                        fabric_addressing_policy=module.params['design_template']['fabric_addressing_policy'],
                                        rack_type_counts=module.params['design_template']['rack_type_counts'],
                                        rack_types=module.params['design_template']['rack_types'],
                                        spine=module.params['design_template']['spine'],
                                        type=module.params['design_template']['type'],
                                        virtual_network_policy=module.params['design_template']['virtual_network_policy']
            )

            response = rest.post(f"design/templates", data=design_element_data)
            # design_element_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=design_element)


def core(module):
    # #######################################################################
    # this is where we take in AnsibleModule class created earlier in the
    # main function, when we inserted our argument spec into it.
    # we'll use new object for all API calls
    # #######################################################################
    rest = ApstraHelper(module)

    # #######################################################################
    # gather a list of sites already created
    # make sure the status code received was a 200
    # store the list of sites in a new object called 'sites', make sure that
    #   the object is in the format of a list, since we'll be looping soon
    # #######################################################################
    response = rest.get(f"design/{module.params['type']}")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive a response from the API, here is the response information to help you debug : {response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    if module.params['type'] == 'logical-devices':
        logical_device(resources, module, rest)
    elif module.params['type'] == 'interface-maps':
        interface_maps(resources, module, rest)
    elif module.params['type'] == 'rack-types':
        rack_types(resources, module, rest)
    elif module.params['type'] == 'templates':
        templates(resources, module, rest)

    module.exit_json(changed=False, data=resources)


def main():
    # #######################################################################
    # this is the main function, did the name give it away?
    # we're taking in the Module's argument spec from the ApstraHelper and
    #   saving it as a new object named 'argument_spec'.
    # another object is created, this time to the specification defined by
    #   the offical AnsibleModule class, and we pass in the argument_spec.
    #   this act creates our new 'module' object, which is then passed
    #   through our other, much larger, function named 'core'
    # #######################################################################
    argument_spec = ApstraHelper.design_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
