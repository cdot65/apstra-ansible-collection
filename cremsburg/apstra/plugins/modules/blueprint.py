#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: design

short_description: Manage Apstra Blueprints.

version_added: "0.0.15"

description: This module will leverage Apstra's REST API to automate the management of Blueprints within Apstra.

options:
    api_token:
        description:
          - used to authenticate to the API
        required: true
        type: str
    display_name:
        description:
            - the name you would like to associate to these networks goes here
        required: true
        type: str
    label:
        description:
          - label name
        required: false
        type: str
    name:
        required=False,
        type='str'
    server:
        description:
            - DNS hostname or IP address of your Apstra Apstra server
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
    - cremsburg.apstra.blueprint

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
    ### # CREATE BLUEPRINT
    ### #################################################################
    - name: "### CREATE IP POOL cicd_leaf_loopbacks"
      cremsburg.apstra.blueprint:

        # define apstra server parameters
        server: "apstra.dmz.home"
        api_token: "{{ api_token }}"

        # define request
        blueprint: "cicd_leaf_loopbacks"

'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.apstra.plugins.module_utils.apstra.api import ApstraHelper
from ansible.module_utils._text import to_native


def build_blueprint(resources, module, rest):
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
            response = rest.delete(f"blueprints/{design_element['id']}")
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
            design_element_data = dict(design=module.params['design'],
                                       init_type=module.params['init_type'],
                                       template_id=module.params['template_id'],
                                       label=module.params['label'])

            response = rest.post(f"blueprints", data=design_element_data)

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
    response = rest.get(f"blueprints")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive a response from the API, here is the response information to help you debug : {response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    build_blueprint(resources, module, rest)

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
    argument_spec = ApstraHelper.blueprint_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
