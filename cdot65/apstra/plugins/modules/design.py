"""
Ansible module to build design elements within Apstra
Copyright: (c) 2022, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com.com>
GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
#!/usr/bin/python

from __future__ import absolute_import, division, print_function
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule  # pylint: disable=import-error
from ansible.module_utils._text import to_native  # pylint: disable=import-error
from ansible_collections.cdot65.apstra.plugins.module_utils.apstra.api import ApstraHelper  # pylint: disable=import-error

__metaclass__ = type  # pylint: disable=invalid-name


DOCUMENTATION = r"""
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
    - cdot65.apstra.design

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.resources:

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
      cdot65.apstra.design:

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
      cdot65.apstra.design:

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
      cdot65.apstra.design:

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
      cdot65.apstra.design:

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
      cdot65.apstra.design:

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
      cdot65.apstra.design:

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

"""


def interface_maps(resources, module, rest):
    """Here we create, update, or delete external routers.

    --------------------------------------------------------------------------
    Determine if the external router already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the external router
      - if False, report back that external router didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the external router
      - if False, create the new external router

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the external router
      - if False, create the new external router
    """
    interface_mapping = {}
    interface_mapping["id"] = None
    interface_mapping["label"] = None
    interface_mapping["provisioned"] = False

    for each in resources["items"]:
        if each["label"] == module.params["label"]:
            interface_mapping["id"] = each["id"]
            interface_mapping["label"] = each["label"]
            interface_mapping["provisioned"] = True

    if module.params["state"] == "absent":
        if interface_mapping["provisioned"] is True:
            response = rest.delete(
                f"design/interface-maps/{interface_mapping['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="Interface Mapping does not exist"
            )

    else:
        if interface_mapping["provisioned"] is False:

            # creating an ID if none exists
            interface_mapping_id = ""
            if module.params["id"] is True:
                interface_mapping_id = module.params["id"]
            else:
                interface_mapping_id = module.params["label"]

            # setting parameters to create interface mapping
            interface_mapping_data = dict(
                device_profile_id=module.params["device_profile_id"],
                id=interface_mapping_id,
                logical_device_id=module.params["logical_device_id"],
                interfaces=module.params["interfaces"],
                label=module.params["label"],
            )

            # create the interface-map and store the response of our API
            response = rest.post("design/interface-maps",
                                 data=interface_mapping_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=interface_mapping)


def logical_device(resources, module, rest):
    """Here we create, update, or delete external routers.

    --------------------------------------------------------------------------
    Determine if the external router already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the external router
      - if False, report back that external router didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the external router
      - if False, create the new external router

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the external router
      - if False, create the new external router
    """
    device = {}
    device["display_name"] = None
    device["id"] = None
    device["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            device["display_name"] = each["display_name"]
            device["id"] = each["id"]
            device["provisioned"] = True

    if module.params["state"] == "absent":
        if device["provisioned"] is True:
            response = rest.delete(
                f"design/logical-devices/{device['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="Logical Device does not exist, exiting"
            )

    else:
        if device["provisioned"] is False:

            # creating an ID if none exists
            logical_device_id = str()
            if module.params["id"] is True:
                logical_device_id = module.params["id"]
            else:
                logical_device_id = module.params["display_name"]

            # setting parameters to create device
            device_data = dict(
                display_name=module.params["display_name"],
                id=logical_device_id,
                panels=module.params["panels"],
            )

            # create the logical-device and store the response of our API
            response = rest.post("design/logical-devices",
                                 data=device_data)
            device_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=device)


def core(module):
    """The core function of our module.

    --------------------------------------------------------------------------
    Gather a list of rack types already created
    --------------------------------------------------------------------------
      - create `rest` object for API call
      - perform a get request
      - store the response in a new object called 'response'
      - ensure the status code received was a 200
      - deserialze the json into the 'resources' object
        - fail if this step does not return a dictionary

    --------------------------------------------------------------------------
    Create, Update, or Delete Resource
    --------------------------------------------------------------------------
      - execute the function that matches the user's `type`
      - exit execution gracefully

    """
    rest = ApstraHelper(module)

    response = rest.get(f"design/{module.params['type']}")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive a response from the API:\n{response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    if module.params["type"] == "logical-devices":
        logical_device(resources, module, rest)
    elif module.params["type"] == "interface-maps":
        interface_maps(resources, module, rest)

    module.exit_json(changed=False, data=resources)


def main():
    """Our module's main execution.

    --------------------------------------------------------------------------
    Creating our argument specification
    --------------------------------------------------------------------------
      - take in the data model from ApstraHelper's `design_spec` method
      - save it as a new object named 'argument_spec'

    --------------------------------------------------------------------------
    Creating our AnsibleModule object
    --------------------------------------------------------------------------
      - pass our `argument_spec` object into AnsibleModule class object
      - store the resulting module object as `module`

    --------------------------------------------------------------------------
    Calling our module object
    --------------------------------------------------------------------------
      - pass our `module` object into our `core` function
      - gracefully fail if an exception appears
    """
    argument_spec = ApstraHelper.design_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception:  # pylint: disable=broad-except
        module.fail_json(msg=to_native(Exception), exception=format_exc())


if __name__ == "__main__":
    main()
