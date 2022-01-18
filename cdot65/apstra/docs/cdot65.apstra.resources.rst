==========================
cdot65.apstra.resources
==========================

---------------------
Manage your resources
---------------------

resources
=========

This module will allow you to manage your resources within AIS.

Feature set as of version 0.0.7:
  - manage all resources
  - supports tagging
  - idempotent

Suported Resources:

================  ============================================================
Resource Type     How to specify within Ansible module parameter "type"
================  ============================================================
ASN Pool          :type: asn-pools
External Routers  :type: external-routers
IPv4 Pool         :type: ip-pools
IPv6 Pool         :type: ipv6-pools
VLAN Pool         :type: vlan-pools
VNI Pool          :type: vni-pools
================  ============================================================

Under construction

Example
-------

Here is a basic example of using the module to mange your resources in Apstra

.. code-block:: yaml

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
        ### # CREATE IP POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Create an IP Pool Resource with two prefixes
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            tags: []
            type: "ip-pools"
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
        ### # CREATE ASN POOL RESOURCES ON APSTRA SERVER
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
        ### # CREATE VNI POOL RESOURCES ON APSTRA SERVER
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
        ### # CREATE VLAN POOL RESOURCES ON APSTRA SERVER
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
        ### # CREATE EXTERNAL ROUTER RESOURCE ON APSTRA SERVER
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

    ### #################################################################
    ### # DELETE RESOURCES PLAY
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
        ### # DELETE IP POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Delete an IP Pool Resource with two prefixes
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "ip-pools"

            # state whether you want to create or delete this resource
            state: absent
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_ippool

        - debug:
            msg: "{{ cicd_test_ippool }}"

        ### #################################################################
        ### # DELETE IPv6 POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Delete an IP Pool Resource with two prefixes
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "ipv6-pools"

            # state whether you want to create or delete this resource
            state: absent
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_ipv6_pool

        - debug:
            msg: "{{ cicd_test_ipv6_pool }}"

        ### #################################################################
        ### # DELETE ASN POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Delete an ASN Pool Resource with two ranges
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "asn-pools"

            # state whether you want to create or delete this resource
            state: absent

          # store the output of our task as a new variable to debug later
          register: cicd_test_asn_pool

        - debug:
            msg: "{{ cicd_test_asn_pool }}"

        ### #################################################################
        ### # DELETE VNI POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Delete an VNI Pool Resource with two ranges
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "vni-pools"

            # state whether you want to create or delete this resource
            state: absent

          # store the output of our task as a new variable to debug later
          register: cicd_test_vni_pool

        - debug:
            msg: "{{ cicd_test_vni_pool }}"

        ### #################################################################
        ### # DELETE VNI POOL RESOURCES ON APSTRA SERVER
        ### #################################################################
        - name: Delete an VLAN Pool Resource with two ranges
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "vlan-pools"

            # state whether you want to create or delete this resource
            state: absent

          # store the output of our task as a new variable to debug later
          register: cicd_test_vlan_pool

        - debug:
            msg: "{{ cicd_test_vlan_pool }}"

        ### #################################################################
        ### # DELETE EXTERNAL ROUTER RESOURCE ON APSTRA SERVER
        ### #################################################################
        - name: Delete an External Router Resource
          cdot65.apstra.resources:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define resource allocations
            display_name: "cicd_test"
            type: "external-routers"

            # state whether you want to create or delete this resource
            state: absent

          # store the output of our task as a new variable to debug later
          register: cicd_test_vlan_pool

        - debug:
            msg: "{{ cicd_test_vlan_pool }}"


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def resources_spec():
        return dict(
            address=dict(
                required=False,
                type='str'),
            asn=dict(
                required=False,
                type='int'),
            api_token=dict(
                required=True,
                fallback=(env_fallback, ['APSTRA_API_TOKEN', 'APSTRA_API_TOKEN', 'API_TOKEN']),
                no_log=True,
                type='str'),
            display_name=dict(
                required=True,
                fallback=(env_fallback, ['APSTRA_USERNAME', 'APSTRA_USERNAME', 'USERNAME']),
                type='str'),
            ipv6_address=dict(
                required=False,
                type='str'),
            port=dict(
                required=True,
                type='int'),
            ranges=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    first=dict(
                        required=True,
                        type='int'),
                    last=dict(
                        required=True,
                        type='int'),
                    ),
                ),
            server=dict(
                required=False,
                type='str'),
            state=dict(
                required=False,
                choices=['absent', 'present'],
                type='str'),
            subnets=dict(
                required=False,
                type='list',
                elements='str'),
            tags=dict(
                required=False,
                type='list',
                elements='str'),
            type=dict(
                required=True,
                choices=['asn-pools', 'external-routers', 'ip-pools', 'ipv6-pools', 'vlan-pools', 'vni-pools'],
                type='str'),
            validate_certs=dict(
                type='bool',
                required=False,
                default=False),
        )
