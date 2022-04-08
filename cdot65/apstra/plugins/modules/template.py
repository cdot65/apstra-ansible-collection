"""
Ansible module to build design templates within Apstra
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
module: template

short_description: Build Design Templates.

version_added: "0.0.10"

description: This module will leverage the platform REST API to automate the management of design templates within Apstra.

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
    - cdot65.apstra.template

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
### #################################################################
### # CREATE RACK PLAY
### #################################################################
    - name: "create design template Redtail_Edge"
      cdot65.apstra.template:
        # apstra server parameters
        server: "{{ apstra_server }}"
        api_token: "{{ api_token }}"

        # request
        display_name: "Redtail_Edge"
        id: "Redtail_Edge"
        type: "l3_collapsed"
        mesh_link_speed:
          value: 10
          unit: "G"
        mesh_link_count: 1
        dhcp_service_intent:
          active: true
        rack_type_counts:
          - rack_type_id: "Redtail_Edge_Rack"
            count: 1
        virtual_network_policy:
          overlay_control_protocol: "evpn"
        rack_types:
          - id: "Redtail_Edge_Rack"
            display_name: "Redtail_Edge_Rack"
            description: "Two Leafs, Two Access with ESI"
            tags: []
            leafs:
              - tags: []
                link_per_spine_count: 0
                redundancy_protocol: "esi"
                leaf_leaf_link_speed: null
                leaf_leaf_l3_link_count: 0
                leaf_leaf_l3_link_speed: null
                link_per_spine_speed: null
                label: "leaf"
                leaf_leaf_l3_link_port_channel_id: 0
                leaf_leaf_link_port_channel_id: 0
                logical_device: "Redtail_vQFX"
                leaf_leaf_link_count: 0
            logical_devices:
              - display_name: "AOS-2x10-1"
                id: "AOS-2x10-1"
                panels:
                  - panel_layout:
                      row_count: 1
                      column_count: 2
                    port_indexing:
                      order: "T-B, L-R"
                      start_index: 1
                      schema: "absolute"
                    port_groups:
                      - count: 2
                        speed:
                          unit: "G"
                          value: 10
                        roles:
                          - "leaf"
                          - "access"
              - display_name: "Redtail_vQFX"
                id: "Redtail_vQFX"
                panels:
                  - panel_layout:
                      row_count: 1
                      column_count: 12
                    port_indexing:
                      order: "T-B, L-R"
                      start_index: 1
                      schema: "absolute"
                    port_groups:
                      - count: 11
                        speed:
                          unit: "G"
                          value: 10
                        roles:
                          - "leaf"
                          - "generic"
                          - "access"
                      - count: 1
                        speed:
                          unit: "G"
                          value: 10
                        roles:
                          - "peer"
            access_switches:
              - tags: []
                redundancy_protocol: esi
                access_access_link_count: 1
                label: access
                logical_device: "Redtail_vQFX"
                links:
                  - tags: []
                    link_per_switch_count: 1
                    label: fabric
                    link_speed:
                      unit: G
                      value: 10
                    target_switch_label: leaf
                    attachment_type: dualAttached
                    lag_mode: lacp_active
                instance_count: 1
                access_access_link_speed:
                  unit: G
                  value: 10
            fabric_connectivity_design: "l3collapsed"
            servers: []
            generic_systems:
              - tags: []
                loopback: disabled
                asn_domain: disabled
                port_channel_id_max: 0
                label: openshift
                count: 1
                management_level: unmanaged
                logical_device: AOS-2x10-1
                links:
                  - tags: []
                    link_per_switch_count: 1
                    label: access
                    link_speed:
                      unit: G
                      value: 10
                    target_switch_label: access
                    attachment_type: dualAttached
                    lag_mode: static_lag
                port_channel_id_min: 0
              - tags: []
                loopback: disabled
                asn_domain: disabled
                port_channel_id_max: 0
                label: rhel
                count: 1
                management_level: unmanaged
                logical_device: AOS-2x10-1
                links:
                  - tags: []
                    link_per_switch_count: 1
                    label: access
                    link_speed:
                      unit: G
                      value: 10
                    switch_peer: second
                    target_switch_label: access
                    attachment_type: singleAttached
                    lag_mode:
                port_channel_id_min: 0

        # to delete or create
        state: "present"
"""


def design_template(resources, module, rest):
    """Here we create, update, or delete design templates.

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
    template = {}
    template["id"] = None
    template["provisioned"] = False

    for each in resources["items"]:
        if each["id"] == module.params["id"]:
            template["id"] = each["id"]
            template["provisioned"] = True

    if module.params["state"] == "absent":
        if template["provisioned"] is True:
            response = rest.delete(f"design/templates/{template['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="Rack Type does not exist, exiting")

    else:
        if template["provisioned"] is False:
            template_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                type=module.params["type"],
                mesh_link_speed=module.params["mesh_link_speed"],
                mesh_link_count=module.params["mesh_link_count"],
                dhcp_service_intent=module.params["dhcp_service_intent"],
                rack_type_counts=module.params["rack_type_counts"],
                virtual_network_policy=module.params["virtual_network_policy"],
                rack_types=module.params["rack_types"],
            )

            response = rest.post("design/templates", data=template_data)

            module.exit_json(changed=True, data=response.json)

        else:
            template_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                type=module.params["type"],
                mesh_link_speed=module.params["mesh_link_speed"],
                mesh_link_count=module.params["mesh_link_count"],
                dhcp_service_intent=module.params["dhcp_service_intent"],
                rack_type_counts=module.params["rack_type_counts"],
                virtual_network_policy=module.params["virtual_network_policy"],
                rack_types=module.params["rack_types"],
            )

            response = rest.put(
                f"design/templates/{template_data['id']}", data=template_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=template)


def core(module):
    """The core function of our module.

    --------------------------------------------------------------------------
    Gather a list of design templates already created
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
      - execute the `design_template` function declared above
      - exit execution gracefully

    """
    rest = ApstraHelper(module)

    response = rest.get("design/templates")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive a response from the API:\n{response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format")

    design_template(resources, module, rest)

    module.exit_json(changed=False, data=resources)


def main():
    """Our module's main execution.

    --------------------------------------------------------------------------
    Creating our argument specification
    --------------------------------------------------------------------------
      - take in the data model from ApstraHelper's `design_template_spec`
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
    argument_spec = ApstraHelper.design_template_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception:  # pylint: disable=broad-except
        module.fail_json(msg=to_native(Exception), exception=format_exc())


if __name__ == "__main__":
    main()
