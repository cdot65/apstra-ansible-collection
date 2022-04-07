"""Ansible module for managing blueprints."""
#!/usr/bin/python

# Copyright: (c) 2022, Calvin Remsburg (@cdot65) <cremsburg.dev@gmail.com>
from __future__ import absolute_import, division, print_function
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule  # pylint: disable=import-error
from ansible_collections.cdot65.apstra.plugins.module_utils.apstra.api import ApstraHelper  # pylint: disable=import-error
from ansible.module_utils._text import to_native  # pylint: disable=import-error disable=ungrouped-imports


__metaclass__ = type  # pylint: disable=invalid-name

DOCUMENTATION = r"""
---
module: design

short_description: Manage Apstra Blueprints.

version_added: "0.0.1"

description: Automate the creation of Blueprints within Apstra.

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
    - cdot65.apstra.blueprint

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
"""


def build_blueprint(resources, module, rest):
    """Building the blueprint within Apstra."""
    design_element = {}
    design_element["id"] = None
    design_element["label"] = None
    design_element["provisioned"] = False
    for each in resources["items"]:
        if each["label"] == module.params["label"]:
            design_element["id"] = each["id"]
            design_element["label"] = each["label"]
            design_element["provisioned"] = True

    # #########################################################################
    # if the user set the state to 'absent', then we need to either delete an
    #   blueprint site, or report back that the blueprint didn't exist.
    # #########################################################################
    if module.params["state"] == "absent":
        if design_element["provisioned"] is True:
            response = rest.delete(f"blueprints/{design_element['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="Blueprint does not exist, exiting")

    # #######################################################################
    # looking to either create or update a blueprint
    # #######################################################################
    else:

        # #####################################################################
        # validate that the Blueprint does not exist before building it out.
        # #####################################################################
        if design_element["provisioned"] is False:

            # #######################################################################
            # design_element_data will be filled by parameters passed into the module
            # #######################################################################
            design_element_data = dict(
                design=module.params["design"],
                id=module.params["label"],
                init_type=module.params["init_type"],
                template_id=module.params["template_id"],
                label=module.params["label"],
            )

            # #################################################################
            # perform the HTTP POST method, passing our parameters as the body.
            # #################################################################
            response = rest.post("blueprints", data=design_element_data)

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=design_element)


def core(module):
    """Core functionality of our module."""

    # create a new object based on the ApstraHelper class object, passing in our module
    rest = ApstraHelper(module)

    # #########################################################################
    # gather a list of blueprints already created
    # make sure the status code received was a 200
    # store the list of sites in a new object called 'response', make sure that
    #   the object is in the format of a dictionary
    # #########################################################################
    response = rest.get("blueprints")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive a proper response from the API: {response.info}")

    resources = response.json

    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg="The response returned is not in a dictionary format, contant support")

    build_blueprint(resources, module, rest)

    module.exit_json(changed=False, data=resources)


def main():
    """The main function will be what is called when executed."""

    # #######################################################################
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
    except Exception as exception_error:  # pylint: disable=broad-except
        module.fail_json(msg=to_native(exception_error), exception=format_exc())


if __name__ == "__main__":
    main()
