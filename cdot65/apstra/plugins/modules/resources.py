"""
Ansible module to build resources within Apstra
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
module: resources

short_description: Manage Resources within Apstra.

version_added: "0.0.1"

description: This module will leverage Apstra's REST API to automate the creation of resources within Apstra.

options:
    address:
        description:
          - IPv4 address for external router loopback address
        required: false
        type: str
    asn:
        description:
          - ASN used by external router
        required: false
        type: int
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
    ipv6_address:
        description:
          - IPv6 address for external router loopback address
        required: false
        type: str
    port:
        description:
            - port number (integer) used by the Apstra AIS server
            - defaults to 443
        required: true
        type: int
    ranges:
        description:
            - first and last integers within a range
        required: true
        type: list
        elements: dict
        options:
            first:
                description:
                  - first object within list
                required: true
                type: int
            last:
                description:
                  - last object within list
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
    subnets:
        description:
            - list the subnets that you would like to have created here
        required: false
        type: list
        elements: dict
        suboptions:
            network:
                required: false
                type: str
    tags:
        description:
            - list any tags that you would like to associate with these networks
        required: false
        type: int
    type:
        description:
            - specify which type of resource you would like to manage
        required: true
        choices:
          - 'asn-pools'
          - 'external-routers'
          - 'ip-pools'
          - 'ipv6-pools'
          - 'vlan-pools'
          - 'vni-pools'
        type: str
    validate_certs:
        description:
            - whether or not the certificate is valid
            - may help those behind proxies
        required: false
        default: true
        type: bool

extends_documentation_fragment:
    - cdot65.apstra.resources

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
### #################################################################
# AUTHENTICATE AND RECEIVE AN API TOKEN FROM THE APSTRA SERVER
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

# ################################################################
# CREATE IP POOL RESOURCES ON APSTRA SERVER
# ################################################################
- name: create an IP Pool Resource with two prefixes
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    type: "ip-pool"
    subnets:
        - "100.1.1.0/24"
        - "100.1.2.0/24"

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_ippool

- debug:
    msg: "{{ cicd_test_ippool }}"

### #################################################################
# CREATE IPv6 POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an IPv6 Pool Resource with two prefixes
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    validate_certs: False
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    tags: []
    type: "ipv6-pools"
    subnets:
        - "2001:db8::192:168:10:251/112"
        - "2001:db8::192:168:20:251/112"

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_ippool

- debug:
    msg: "{{ cicd_test_ippool }}"

### #################################################################
# CREATE ASN POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an ASN Pool Resource with two ranges
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    validate_certs: False
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    tags: []
    type: "asn-pools"
    ranges:
        - first: 65300
        last: 65399
        - first: 65500
        last: 65599

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_asn_pool

- debug:
    msg: "{{ cicd_test_asn_pool }}"

### #################################################################
# CREATE VNI POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an VNI Pool Resource with two ranges
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    validate_certs: False
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    tags: []
    type: "vni-pools"
    ranges:
        - first: 65300
        last: 65399
        - first: 65500
        last: 65599

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_vni_pool

- debug:
    msg: "{{ cicd_test_vni_pool }}"

### #################################################################
# CREATE VLAN POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an VLAN Pool Resource with two ranges
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    validate_certs: False
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    tags: []
    type: "vlan-pools"
    ranges:
        - first: 3990
        last: 3999
        - first: 4070
        last: 4079

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_vlan_pool

- debug:
    msg: "{{ cicd_test_vlan_pool }}"

### #################################################################
# CREATE EXTERNAL ROUTER RESOURCE ON APSTRA SERVER
### #################################################################
- name: Create an External Router Resource
    cdot65.apstra.resources:
    # define server connectivity options
    server: apstra.dmz.home
    port: 443
    validate_certs: False
    api_token: "{{ api_token }}"

    # define resource allocations
    display_name: "cicd_test"
    address: "192.168.10.255"
    ipv6_address: "fc01:a05:192:168:10::255"
    asn: 65000
    type: "external-routers"

    # state whether you want to create or delete this resource
    state: present

    # store the output of our task as a new variable to debug later
    register: cicd_test_external_routers

- debug:
    msg: "{{ cicd_test_external_routers }}"


"""


def external_routers(resources, module, rest):
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
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    external_router = dict()
    external_router["display_name"] = None
    external_router["id"] = None
    external_router["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            external_router["display_name"] = each["display_name"]
            external_router["id"] = each["id"]
            external_router["provisioned"] = True

    if module.params["state"] == "absent":
        if external_router["provisioned"] is True:
            response = rest.delete(
                f"resources/external-routers/{external_router['id']}"
            )
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="External Router does not exist, exiting"
            )

    else:
        if external_router["provisioned"] is False:

            # setting parameters to create the router
            router_data = dict(
                display_name=module.params["display_name"],
                asn=module.params["asn"],
                id=module.params["id"],
                address=module.params["address"],
                ipv6_address=module.params["ipv6_address"],
            )

            # create the router and store the response of our API
            response = rest.post(
                "resources/external-routers", data=router_data
            )
            router_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=external_router)


def ipv4_pool(resources, module, rest):
    """Here we create, update, or delete IPv4 pools.

    --------------------------------------------------------------------------
    Determine if the IP pool already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the IP pool
      - if False, report back that IP pool didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the IP pool
      - if False, create the new IP pool

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the IP pool
      - if False, create the new IP pool
    """
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format."
        )

    pool = {}
    pool["display_name"] = None
    pool["id"] = None
    pool["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            pool["display_name"] = each["display_name"]
            pool["id"] = each["id"]
            pool["provisioned"] = True

    if module.params["state"] == "absent":
        if pool["provisioned"] is True:
            response = rest.delete(f"resources/ip-pools/{pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="IP Pool does not exist, exiting")

    else:
        if pool["provisioned"] is False:

            # changing the data-model of the subnets for API
            subnets_payload = []
            for each in module.params["subnets"]:
                networks = {}
                networks["network"] = each
                subnets_payload.append(networks)

            # setting parameters to create the pool
            pool_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                subnets=subnets_payload,
                tags=module.params["tags"],
            )

            # create the pool and store the response of our API
            response = rest.post("resources/ip-pools", data=pool_data)
            pool_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=pool)


def ipv6_pool(resources, module, rest):
    """Here we create, update, or delete IPv6 pools.

    --------------------------------------------------------------------------
    Determine if the IP pool already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the IP pool
      - if False, report back that IP pool didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the IP pool
      - if False, create the new IP pool

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the IP pool
      - if False, create the new IP pool
    """
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    pool = {}
    pool["display_name"] = None
    pool["id"] = None
    pool["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            pool["display_name"] = each["display_name"]
            pool["id"] = each["id"]
            pool["provisioned"] = True

    if module.params["state"] == "absent":
        if pool["provisioned"] is True:
            response = rest.delete(f"resources/ipv6-pools/{pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="IPv6 Pool does not exist, exiting")

    else:
        if pool["provisioned"] is False:

            # changing the data-model of the subnets for API
            subnets_payload = list()
            for each in module.params["subnets"]:
                networks = dict()
                networks["network"] = each
                subnets_payload.append(networks)

            # setting parameters to create the pool
            pool_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                subnets=subnets_payload,
                tags=module.params["tags"],
            )

            # create the pool and store the response of our API
            response = rest.post("resources/ipv6-pools", data=pool_data)
            pool_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=pool)


def asn_pool(resources, module, rest):
    """Here we create, update, or delete ASN pools.

    --------------------------------------------------------------------------
    Determine if the ASN pool already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the ASN pool
      - if False, report back that ASN pool didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the ASN pool
      - if False, create the new ASN pool

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the ASN pool
      - if False, create the new ASN pool
    """
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    pool = {}
    pool["display_name"] = None
    pool["id"] = None
    pool["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            pool["display_name"] = each["display_name"]
            pool["id"] = each["id"]
            pool["provisioned"] = True

    if module.params["state"] == "absent":
        if pool["provisioned"] is True:
            response = rest.delete(f"resources/asn-pools/{pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="ASN Pool does not exist, exiting")

    else:
        if pool["provisioned"] is False:
            # setting parameters to create the pool
            pool_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                ranges=module.params["ranges"],
                tags=module.params["tags"],
            )

            # create the pool and store the response of our API
            response = rest.post("resources/asn-pools", data=pool_data)
            pool_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=pool)


def vlan_pool(resources, module, rest):
    """Here we create, update, or delete VLAN pools.

    --------------------------------------------------------------------------
    Determine if the VLAN pool already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the VLAN pool
      - if False, report back that VLAN pool didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the VLAN pool
      - if False, create the new VLAN pool

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the VLAN pool
      - if False, create the new VLAN pool
    """
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    pool = {}
    pool["display_name"] = None
    pool["id"] = None
    pool["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            pool["display_name"] = each["display_name"]
            pool["id"] = each["id"]
            pool["provisioned"] = True

    if module.params["state"] == "absent":
        if pool["provisioned"] is True:
            response = rest.delete(f"resources/vlan-pools/{pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="VLAN Pool does not exist, exiting")

    else:
        if pool["provisioned"] is False:

            # setting parameters to create the pool
            pool_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                ranges=module.params["ranges"],
                tags=module.params["tags"],
            )

            # create the pool and store the response of our API
            response = rest.post("resources/vlan-pools", data=pool_data)
            pool_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=pool)


def vni_pool(resources, module, rest):
    """Here we create, update, or delete VNI pools.

    --------------------------------------------------------------------------
    Determine if the VNI pool already exists
    --------------------------------------------------------------------------
      - create a new dictionary with a k/v of 'provisioned' set to False
      - set to True if the resource has already been provisioned
      - store it's ID

    --------------------------------------------------------------------------
    If the user set the state to 'absent'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we delete the VNI pool
      - if False, report back that VNI pool didn't exist

    --------------------------------------------------------------------------
    If the user set the state to 'present'
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the VNI pool
      - if False, create the new VNI pool

    --------------------------------------------------------------------------
    Passing user's arguments into the module
    --------------------------------------------------------------------------
      - check the value of 'provisioned'
      - if True, we will find the ID and update the VNI pool
      - if False, create the new VNI pool
    """
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(
            msg="The response returned is not in a dictionary format"
        )

    pool = {}
    pool["display_name"] = None
    pool["id"] = None
    pool["provisioned"] = False

    for each in resources["items"]:
        if each["display_name"] == module.params["display_name"]:
            pool["display_name"] = each["display_name"]
            pool["id"] = each["id"]
            pool["provisioned"] = True

    if module.params["state"] == "absent":
        if pool["provisioned"] is True:
            response = rest.delete(f"resources/vni-pools/{pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(
                changed=False, data="VNI Pool does not exist, exiting")

    else:
        if pool["provisioned"] is False:

            # setting parameters to create the pool
            pool_data = dict(
                display_name=module.params["display_name"],
                id=module.params["id"],
                ranges=module.params["ranges"],
                tags=module.params["tags"],
            )

            # create the pool and store the response of our API
            response = rest.post("resources/vni-pools", data=pool_data)
            pool_data["id"] = response.json["id"]

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=pool)


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

    response = rest.get(f"resources/{module.params['type']}")
    if response.status_code != 200:
        module.fail_json(
            msg=f"Failed to receive a response from the API:\n{response.info}")

    resources = response.json

    if module.params["type"] == "ip-pools":
        ipv4_pool(resources, module, rest)
    elif module.params["type"] == "ipv6-pools":
        ipv6_pool(resources, module, rest)
    elif module.params["type"] == "external-routers":
        external_routers(resources, module, rest)
    elif module.params["type"] == "asn-pools":
        asn_pool(resources, module, rest)
    elif module.params["type"] == "vlan-pools":
        vlan_pool(resources, module, rest)
    elif module.params["type"] == "vni-pools":
        vni_pool(resources, module, rest)

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
    argument_spec = ApstraHelper.resources_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception:  # pylint: disable=broad-except
        module.fail_json(msg=to_native(Exception), exception=format_exc())


if __name__ == "__main__":
    main()
