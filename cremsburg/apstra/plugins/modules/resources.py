#!/usr/bin/python

# Copyright: (c) 2020, Calvin Remsburg (@cremsburg) <cremsburg@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
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
    - cremsburg.apstra.resources

author:
    - Calvin Remsburg (@cremsburg)
'''

EXAMPLES = r'''
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

# ################################################################
# CREATE IP POOL RESOURCES ON APSTRA SERVER
# ################################################################
- name: create an IP Pool Resource with two prefixes
    cremsburg.apstra.resources:
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
### # CREATE IPv6 POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an IPv6 Pool Resource with two prefixes
    cremsburg.apstra.resources:
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
### # CREATE ASN POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an ASN Pool Resource with two ranges
    cremsburg.apstra.resources:
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
### # CREATE VNI POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an VNI Pool Resource with two ranges
    cremsburg.apstra.resources:
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
### # CREATE VLAN POOL RESOURCES ON APSTRA SERVER
### #################################################################
- name: Create an VLAN Pool Resource with two ranges
    cremsburg.apstra.resources:
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
### # CREATE EXTERNAL ROUTER RESOURCE ON APSTRA SERVER
### #################################################################
- name: Create an External Router Resource
    cremsburg.apstra.resources:
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


'''


from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cremsburg.apstra.plugins.module_utils.apstra.api import ApstraHelper
from ansible.module_utils._text import to_native


def external_routers(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    external_router = dict()
    external_router['display_name'] = None
    external_router['id'] = None
    external_router['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            external_router['display_name'] = each['display_name']
            external_router['id'] = each['id']
            external_router['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if external_router['provisioned'] is True:
            response = rest.delete(f"resources/external-routers/{external_router['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="External Router does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the external_router if it doesn't already exist
        # #######################################################################
        if external_router['provisioned'] is False:

            # ###########################################################################
            # external_router_data: parameters entered by the user to create the resource
            # ###########################################################################
            external_router_data = dict(display_name=module.params['display_name'],
                                        asn=module.params['asn'],
                                        address=module.params['address'],
                                        ipv6_address=module.params['ipv6_address'])

            response = rest.post(f"resources/external-routers", data=external_router_data)
            external_router_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=external_router)


def ipv4_pool(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the ippool has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    ipv4_pool = dict()
    ipv4_pool['display_name'] = None
    ipv4_pool['id'] = None
    ipv4_pool['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            ipv4_pool['display_name'] = each['display_name']
            ipv4_pool['id'] = each['id']
            ipv4_pool['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if ipv4_pool['provisioned'] is True:
            response = rest.delete(f"resources/ip-pools/{ipv4_pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="IP Pool does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the ipv4_pool if it doesn't already exist
        # #######################################################################
        if ipv4_pool['provisioned'] is False:

            # #######################################################################
            # we create a few important objects here:
            #   - subnets_payload: changing the data-model of the subnets for API
            #   - ipv4_pool_data: parameters entered by the user to create the site
            #   - response: create the site and store the response of our API
            #   - site['id']: use the response to get the site's id
            #                 parent object site was created above
            # #######################################################################
            subnets_payload = list()
            for each in module.params['subnets']:
                networks = dict()
                networks['network'] = each
                subnets_payload.append(networks)

            ipv4_pool_data = dict(display_name=module.params['display_name'],
                                  subnets=subnets_payload,
                                  tags=module.params['tags'])

            response = rest.post(f"resources/ip-pools", data=ipv4_pool_data)
            ipv4_pool_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=ipv4_pool)


def ipv6_pool(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    ipv6_pool = dict()
    ipv6_pool['display_name'] = None
    ipv6_pool['id'] = None
    ipv6_pool['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            ipv6_pool['display_name'] = each['display_name']
            ipv6_pool['id'] = each['id']
            ipv6_pool['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if ipv6_pool['provisioned'] is True:
            response = rest.delete(f"resources/ipv6-pools/{ipv6_pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="IPv6 Pool does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the ipv6_pool if it doesn't already exist
        # #######################################################################
        if ipv6_pool['provisioned'] is False:

            # #######################################################################
            # we create a few important objects here:
            #   - subnets_payload: changing the data-model of the subnets for API
            #   - ipv6_pool_data: parameters entered by the user to create the site
            #   - response: create the site and store the response of our API
            #   - site['id']: use the response to get the site's id
            #                 parent object site was created above
            # #######################################################################
            subnets_payload = list()
            for each in module.params['subnets']:
                networks = dict()
                networks['network'] = each
                subnets_payload.append(networks)

            ipv6_pool_data = dict(display_name=module.params['display_name'],
                                  subnets=subnets_payload,
                                  tags=module.params['tags'])

            response = rest.post(f"resources/ipv6-pools", data=ipv6_pool_data)
            ipv6_pool_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=ipv6_pool)


def asn_pool(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    asn_pool = dict()
    asn_pool['display_name'] = None
    asn_pool['id'] = None
    asn_pool['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            asn_pool['display_name'] = each['display_name']
            asn_pool['id'] = each['id']
            asn_pool['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if asn_pool['provisioned'] is True:
            response = rest.delete(f"resources/asn-pools/{asn_pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="ASN Pool does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the asn_pool if it doesn't already exist
        # #######################################################################
        if asn_pool['provisioned'] is False:

            # #######################################################################
            # we create a few important objects here:
            #   - subnets_payload: changing the data-model of the subnets for API
            #   - asn_pool_data: parameters entered by the user to create the site
            #   - response: create the site and store the response of our API
            #   - site['id']: use the response to get the site's id
            #                 parent object site was created above
            # #######################################################################
            asn_pool_data = dict(display_name=module.params['display_name'],
                                 ranges=module.params['ranges'],
                                 tags=module.params['tags'])

            response = rest.post(f"resources/asn-pools", data=asn_pool_data)
            asn_pool_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=asn_pool)


def vlan_pool(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    vlan_pool = dict()
    vlan_pool['display_name'] = None
    vlan_pool['id'] = None
    vlan_pool['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            vlan_pool['display_name'] = each['display_name']
            vlan_pool['id'] = each['id']
            vlan_pool['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if vlan_pool['provisioned'] is True:
            response = rest.delete(f"resources/vlan-pools/{vlan_pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="VLAN Pool does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the vlan_pool if it doesn't already exist
        # #######################################################################
        if vlan_pool['provisioned'] is False:

            # #######################################################################
            # we create a few important objects here:
            #   - subnets_payload: changing the data-model of the subnets for API
            #   - vlan_pool_data: parameters entered by the user to create the site
            #   - response: create the site and store the response of our API
            #   - site['id']: use the response to get the site's id
            #                 parent object site was created above
            # #######################################################################
            vlan_pool_data = dict(display_name=module.params['display_name'],
                                  ranges=module.params['ranges'],
                                  tags=module.params['tags'])

            response = rest.post(f"resources/vlan-pools", data=vlan_pool_data)
            vlan_pool_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=vlan_pool)


def vni_pool(resources, module, rest):
    if isinstance(resources, dict):
        pass
    else:
        module.fail_json(msg=f"The response returned is not in a dictionary format, contant support")

    # ########################################################################
    # we need to see if our Resource has already been created, this determine
    #   our future API calls.
    # we create a new dictionary with a k/v of 'provisioned' set to False.
    #   if the site has already been provisioned, we'll flip this bit to True
    #   and store it's site ID
    # ########################################################################
    vni_pool = dict()
    vni_pool['display_name'] = None
    vni_pool['id'] = None
    vni_pool['provisioned'] = False
    for each in resources["items"]:
        if each['display_name'] == module.params['display_name']:
            vni_pool['display_name'] = each['display_name']
            vni_pool['id'] = each['id']
            vni_pool['provisioned'] = True

    # #######################################################################
    # if the user set the state to 'absent', then we need to either delete
    #   an existing site, or report back to the user that the site didn't
    #   exist.
    # #######################################################################
    if module.params['state'] == "absent":
        if vni_pool['provisioned'] is True:
            response = rest.delete(f"resources/vni-pools/{vni_pool['id']}")
            module.exit_json(changed=True, data=response.json)
        else:
            module.exit_json(changed=False, data="VNI Pool does not exist, exiting")

    # #######################################################################
    # if you made it here, then you're looking to either create an existing,
    #   or update an existing, ip pool
    # this logic can get a little harry, so stick with the comments when
    #   you're deep in the woods and need a guiding light
    # #######################################################################
    else:

        # #######################################################################
        # create the vni_pool if it doesn't already exist
        # #######################################################################
        if vni_pool['provisioned'] is False:

            # #######################################################################
            # we create a few important objects here:
            #   - subnets_payload: changing the data-model of the subnets for API
            #   - vni_pool_data: parameters entered by the user to create the site
            #   - response: create the site and store the response of our API
            #   - site['id']: use the response to get the site's id
            #                 parent object site was created above
            # #######################################################################
            vni_pool_data = dict(display_name=module.params['display_name'],
                                 ranges=module.params['ranges'],
                                 tags=module.params['tags'])

            response = rest.post(f"resources/vni-pools", data=vni_pool_data)
            vni_pool_data['id'] = response.json['id']

            module.exit_json(changed=True, data=response.json)

        module.exit_json(changed=False, data=vni_pool)


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
    response = rest.get(f"resources/{module.params['type']}")
    if response.status_code != 200:
        module.fail_json(msg=f"Failed to receive a response from the API, here is the response information to help you debug : {response.info}")

    resources = response.json

    if module.params['type'] == 'ip-pools':
        ipv4_pool(resources, module, rest)
    elif module.params['type'] == 'ipv6-pools':
        ipv6_pool(resources, module, rest)
    elif module.params['type'] == 'external-routers':
        external_routers(resources, module, rest)
    elif module.params['type'] == 'asn-pools':
        asn_pool(resources, module, rest)
    elif module.params['type'] == 'vlan-pools':
        vlan_pool(resources, module, rest)
    elif module.params['type'] == 'vni-pools':
        vni_pool(resources, module, rest)

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
    argument_spec = ApstraHelper.resources_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == '__main__':
    main()
