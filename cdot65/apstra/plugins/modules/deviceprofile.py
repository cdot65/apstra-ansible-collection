#!/usr/bin/python

# Copyright: (c) 2022, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: deviceprofile

short_description: Manage Device Profiles within Apstra.

version_added: "0.0.1"

description: This module will leverage Apstra's REST API to automate the management of Device Profiles within Apstra.

options:
    api_token:
        description:
          - used to authenticate to the API
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
    validate_certs:
        description:
            - whether or not the certificate is valid
            - may help those behind proxies
        required: false
        default: true
        type: bool

extends_documentation_fragment:
    - cdot65.apstra.deviceprofile

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
### #################################################################
### # CREATE BLUEPRINT PLAY
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
        url: "https://{{ apstra_server }}/api/user/login"
        method: POST
        headers:
          Content-Type: application/json
        status_code: 201
        validate_certs: False
        body_format: json
        body:
          username: "{{ apstra_user }}"
          password: "{{ apstra_password }}"
      register: api_token

    - name: create 'api_token' object by setting it equal to value in response
      ansible.builtin.set_fact:
        api_token: "{{ api_token.json.token }}"

    ### #################################################################
    ### # CREATE DEVICE PROFILE
    ### #################################################################
    - name: "create device profiles Redtail_vQFX"
      cdot65.apstra.design:
        # apstra server parameters
        server: "{{ apstra_server }}"
        api_token: "{{ api_token }}"

        # request
        type: "device-profiles"
        label: Redtail_vQFX
        id: Redtail_vQFX
        slot_count: 0
        selector:
          os_version: '(1[89]|2[0-2])\..*'
          model: VQFX-10000
          os: Junos
          manufacturer: Juniper
        hardware_capabilities:
          userland: 32
          routing_instance_supported:
            - version: .*
              value: true
          ram: 32
          asic: Q5
          form_factor: 1RU
          ecmp_limit: 32
          cpu: x86
        software_capabilities:
          onie: false
          config_apply_support: complete_only
          lxc_support: false
        ports:
          - port_id: 1
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 1
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/0
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 2
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 2
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/1
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 3
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 3
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/2
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 4
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 4
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/3
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 5
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 5
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/4
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 6
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 6
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/5
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 7
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 7
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/6
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 8
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 8
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/7
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 9
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 9
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/8
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 10
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 10
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/9
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 11
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 11
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/10
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'
          - port_id: 12
            slot_id: 0
            panel_id: 1
            connector_type: sfp
            failure_domain_id: 1
            row_id: 1
            column_id: 12
            transformations:
              - transformation_id: 1
                is_default: true
                interfaces:
                  - interface_id: 1
                    name: xe-0/0/11
                    state: active
                    speed:
                      value: 10
                      unit: G
                    setting: '{"global": {"speed": ""}, "interface": {"speed": ""}}'

        # to delete or create
        state: present
"""


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.apstra.plugins.module_utils.apstra.api import (
    ApstraHelper,
)
from ansible.module_utils._text import to_native


def device_profiles(resources, module, rest):
    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    device_profile = dict()
    device_profile["display_name"] = None
    device_profile["id"] = None
    device_profile["provisioned"] = False
    for each in resources["items"]:
        if each["label"] == module.params["label"]:
            device_profile["label"] = each["label"]
            device_profile["id"] = each["id"]
            device_profile["provisioned"] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params["state"] == "absent":
        if device_profile["provisioned"] is True:
            response = rest.delete(f"device-profiles/{device_profile['id']}")
            if "errors" in response.json:
                module.fail_json(msg=response.json["errors"])
            else:
                module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="Device Profile does not exist, exiting"
            )

    # #######################################################################
    # looking to either create or update a logical device
    # #######################################################################
    else:

        # #######################################################################
        # create the logical device if it doesn't already exist
        # #######################################################################
        if device_profile["provisioned"] is False:

            # ###########################################################################
            # device_profile_data: parameters entered by the user to create the resource
            # ###########################################################################
            device_profile_data = dict(
                label=module.params["label"],
                id=module.params["id"],
                slot_count=module.params["slot_count"],
                selector=module.params["selector"],
                hardware_capabilities=module.params["hardware_capabilities"],
                software_capabilities=module.params["software_capabilities"],
                ports=module.params["ports"],
            )

            response = rest.post(f"device-profiles", data=device_profile_data)
            # device_profile_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=device_profile)


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
    response = rest.get(f"device-profiles")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive a response from the API, here is the response information to help you debug : {response.info}"
        )

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg=f"The response returned is not in a dictionary format, contant support"
        )

    device_profiles(resources, module, rest)

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
    argument_spec = ApstraHelper.device_profiles_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
