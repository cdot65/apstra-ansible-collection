"""
Ansible module to build rack types within Apstra
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
module: rack

short_description: Build Rack Types.

version_added: "0.0.10"

description: This module will leverage the platform REST API to automate the management of Rack Types within Apstra.

options:
    access_switches:
    api_token:
        description:
          - used to authenticate to the API
        required: true
        type: str
    description:
    display_name:
        description:
            - the name you would like to associate to this rack type
        required: true
        type: str
    fabric_connectivity_design:
    generic_systems:
    id:
        description:
          - ID name of rack type
        required: false
        type: str
    leafs:
    logical_devices:
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
    servers:
        required: true
        type: list
    state:
        description:
            - declare whether you want the resource to exist or be deleted
        required: true
        choices:
          - 'absent'
          - 'present'
        type: str
    tags:
        type: list
    validate_certs:
        description:
            - whether or not the certificate is valid
            - may help those behind proxies
        required: false
        default: true
        type: bool

extends_documentation_fragment:
    - cdot65.apstra.rack

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
### #################################################################
### # CREATE RACK PLAY
### #################################################################
- hosts: localhost
  gather_facts: False
  become: False
  tasks:
    - name: "create rack type Redtail_Edge_Rack"
      cdot65.apstra.rack:
        # apstra server parameters
        server: "{{ apstra_server }}"
        api_token: "{{ api_token }}"

        # request
        id: "Redtail_Edge_Rack"
        description: "Two Spines, Two Leafs, ESI"
        display_name: "Redtail Rack Edge"
        fabric_connectivity_design: "l3collapsed"
        access_switches:
          - access_access_link_count: 1
            access_access_link_speed:
              unit: "G"
              value: 10
            instance_count: 1
            label: "access"
            links:
              - attachment_type: "dualAttached"
                label: "fabric"
                lag_mode: "lacp_active"
                link_per_switch_count: 1
                link_speed:
                  unit: "G"
                  value: 10
                tags: []
                target_switch_label: "leaf"
            logical_device: "Redtail_vQFX"
            redundancy_protocol: "esi"
            tags: []

        generic_systems:
          - asn_domain: "disabled"
            count: 1
            label: "openshift"
            links:
              - attachment_type: "dualAttached"
                label: "access"
                lag_mode: "static_lag"
                link_per_switch_count: 1
                link_speed:
                  unit: "G"
                  value: 10
                tags: []
                target_switch_label: "access"
            logical_device: "AOS-2x10-1"
            loopback: "disabled"
            management_level: "unmanaged"
            port_channel_id_max: 0
            port_channel_id_min: 0
            tags: []
          - asn_domain: "disabled"
            count: 1
            label: "rhel"
            links:
              - attachment_type: "singleAttached"
                label: "access"
                lag_mode: null
                link_per_switch_count: 1
                link_speed:
                  unit: "G"
                  value: 10
                switch_peer: "second"
                tags: []
                target_switch_label: "access"
            logical_device: "AOS-2x10-1"
            loopback: "disabled"
            management_level: "unmanaged"
            port_channel_id_max: 0
            port_channel_id_min: 0
            tags: []

        leafs:
          - label: "leaf"
            leaf_leaf_l3_link_count: 0
            leaf_leaf_l3_link_port_channel_id: 0
            leaf_leaf_l3_link_speed: null
            leaf_leaf_link_count: 0
            leaf_leaf_link_port_channel_id: 0
            leaf_leaf_link_speed: null
            link_per_spine_count: 0
            logical_device: "Redtail_vQFX"
            redundancy_protocol: "esi"
            tags: []

        logical_devices:
          - display_name: "AOS-2x10-1"
            id: "AOS-2x10-1"
            panels:
              - panel_layout:
                  column_count: 2
                  row_count: 1
                port_groups:
                  - count: 2
                    roles:
                      - "leaf"
                      - "access"
                    speed:
                      unit: G
                      value: 10
                port_indexing:
                  order: "T-B, L-R"
                  schema: "absolute"
                  start_index: 1
          - display_name: "Redtail_vQFX"
            id: "Redtail_vQFX"
            panels:
              - panel_layout:
                  column_count: 12
                  row_count: 1
                port_groups:
                  - count: 11
                    roles:
                      - "leaf"
                      - "generic"
                      - "access"
                    speed:
                      unit: "G"
                      value: 10
                  - count: 1
                    roles:
                      - "peer"
                    speed:
                      unit: "G"
                      value: 10
                port_indexing:
                  order: "T-B, L-R"
                  schema: "absolute"
                  start_index: 1
          - display_name: "AOS-2x10-1"
            id: "AOS-2x10-1"
            panels:
              - panel_layout:
                  column_count: 2
                  row_count: 1
                port_groups:
                  - count: 2
                    roles:
                      - "leaf"
                      - "access"
                    speed:
                      unit: "G"
                      value: 10
                port_indexing:
                  order: "T-B, L-R"
                  schema: "absolute"
                  start_index: 1
          - display_name: "Redtail_vQFX"
            id: "Redtail_vQFX"
            panels:
              - panel_layout:
                  column_count: 12
                  row_count: 1
                port_groups:
                  - count: 11
                    roles:
                      - "leaf"
                      - "generic"
                      - "access"
                    speed:
                      unit: "G"
                      value: 10
                  - count: 1
                    roles:
                      - "peer"
                    speed:
                      unit: "G"
                      value: 10
                port_indexing:
                  order: "T-B, L-R"
                  schema: "absolute"
                  start_index: 1
        servers: []
        tags: []

        # to delete or create
        state: "present"
"""


def rack_types(resources, module, rest):
    """Here we create, update, or delete Rack Types.

    --------------------------------------------------------------------------
    Determine if the rack type already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's site ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the rack type
      - if False, report back that rack type didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the rack type
      - if False, create the new rack type

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the rack type
      - if False, create the new rack type
    """
    rack_type = {}
    rack_type["id"] = None
    rack_type["provisioned"] = False

    for each in resources["items"]:
        if each["id"] == module.params["id"]:
            rack_type["id"] = each["id"]
            rack_type["provisioned"] = True

    if module.params["state"] == "absent":
        if rack_type["provisioned"] is True:
            response = rest.delete(f"design/rack-types/{rack_type['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="Rack Type does not exist, exiting")

    else:
        if rack_type["provisioned"] is False:
            rack_type_data = dict(
                access_switches=module.params["access_switches"],
                description=module.params["description"],
                display_name=module.params["display_name"],
                fabric_connectivity_design=module.params["fabric_connectivity_design"],
                generic_systems=module.params["generic_systems"],
                id=module.params["id"],
                leafs=module.params["leafs"],
                logical_devices=module.params["logical_devices"],
                servers=module.params["servers"],
                tags=module.params["tags"],
            )

            response = rest.post("design/rack-types", data=rack_type_data)

            module.exit_json(changed=True, data=response.json)

        else:
            rack_type_data = dict(
                access_switches=module.params["access_switches"],
                description=module.params["description"],
                display_name=module.params["display_name"],
                fabric_connectivity_design=module.params["fabric_connectivity_design"],
                generic_systems=module.params["generic_systems"],
                id=module.params["id"],
                leafs=module.params["leafs"],
                logical_devices=module.params["logical_devices"],
                servers=module.params["servers"],
                tags=module.params["tags"],
            )

            response = rest.put(
                f"design/rack-types/{rack_type_data['id']}", data=rack_type_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=rack_type)


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
    Create, Update, or Delete Rack Type
    --------------------------------------------------------------------------
      - execute the `rack_types` function declared above
      - exit execution gracefully

    """
    rest = ApstraHelper(module)

    response = rest.get("design/rack-types")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive a response from the API:\n{response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format")

    rack_types(resources, module, rest)

    module.exit_json(changed=False, data=resources)


def main():
    """Our module's main execution.

    --------------------------------------------------------------------------
    Creating our argument specification
    --------------------------------------------------------------------------
      - take in the data model from ApstraHelper's `rack_spec` method
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
    argument_spec = ApstraHelper.rack_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception:  # pylint: disable=broad-except
        module.fail_json(msg=to_native(Exception), exception=format_exc())


if __name__ == "__main__":
    main()
