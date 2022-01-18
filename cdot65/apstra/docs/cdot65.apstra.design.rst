=======================
cdot65.apstra.design
=======================

-------------------
Manage your designs
-------------------

design
======

This module will allow you to manage your design elements within Apstra.

Feature set as of version 0.0.14:
  - manage Logical Devices, Rack Types, Templates, Intereface Mapping
  - idempotent

Suported Resources:

=================  ============================================================
Design Element     How to specify within Ansible module parameter "type"
=================  ============================================================
Interface Mapping  :type: interface-maps
Logical Device     :type: logical-devices
Rack Types         :type: rack-types
Templates          :type: templates
=================  ============================================================

Under construction

Example
-------

Here is a basic example of using the module to mange your resources in Apstra

.. code-block:: yaml

    ---
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
        ### # CREATE A NEW LOGICAL DEVICE ON APSTRA SERVER
        ### #################################################################
        - name: Create a logical device
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical device)
            type: "logical-devices"
            display_name: "cicd_test"
            panels:
              - panel_layout:
                  row_count: 1
                  column_count: 12
                port_indexing:
                  order: "T-B, L-R"
                  schema: "absolute"
                  start_index: 1
                port_groups:
                  - count: 12
                    roles:
                      - leaf
                    speed:
                      value: 10
                      unit: "G"

            # state whether you want to create or delete this resource
            state: present
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_logical_device

        - debug:
            msg: "{{ cicd_test_logical_device }}"

        ### #################################################################
        ### # CREATE A NEW INTERFACE MAPPING ON APSTRA SERVER
        ### #################################################################
        - name: Create an interface mapping
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical device)
            type: "interface-maps"
            label: "cicd_test"
            logical_device_id: "{{ cicd_test_logical_device['data']['id'] }}"
            device_profile_id: "Juniper_vQFX"
            interfaces:
              - name: "xe-0/0/0"
                roles:
                  - leaf
                mapping: 
                  - 1
                  - 1
                  - 1
                  - 1
                  - 1
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 1
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/1"
                roles:
                  - leaf
                mapping: 
                  - 2
                  - 1
                  - 1
                  - 1
                  - 2
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 2
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/2"
                roles:
                  - leaf
                mapping: 
                  - 3
                  - 1
                  - 1
                  - 1
                  - 3
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 3
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/3"
                roles:
                  - leaf
                mapping: 
                  - 4
                  - 1
                  - 1
                  - 1
                  - 4
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 4
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/4"
                roles:
                  - leaf
                mapping: 
                  - 5
                  - 1
                  - 1
                  - 1
                  - 5
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 5
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/5"
                roles:
                  - leaf
                mapping: 
                  - 6
                  - 1
                  - 1
                  - 1
                  - 6
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 6
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/6"
                roles:
                  - leaf
                mapping: 
                  - 7
                  - 1
                  - 1
                  - 1
                  - 7
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 7
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/7"
                roles:
                  - leaf
                mapping: 
                  - 8
                  - 1
                  - 1
                  - 1
                  - 8
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 8
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/8"
                roles:
                  - leaf
                mapping: 
                  - 9
                  - 1
                  - 1
                  - 1
                  - 9
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 9
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/9"
                roles:
                  - leaf
                mapping: 
                  - 10
                  - 1
                  - 1
                  - 1
                  - 10
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 10
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/10"
                roles:
                  - leaf
                mapping: 
                  - 11
                  - 1
                  - 1
                  - 1
                  - 11
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 11
                speed:
                  unit: "G"
                  value: 10

              - name: "xe-0/0/11"
                roles:
                  - leaf
                mapping: 
                  - 12
                  - 1
                  - 1
                  - 1
                  - 12
                state: "active"
                setting: 
                  param: "{\"interface\": {\"speed\": \"\"}, \"global\": {\"speed\": \"\"}}"
                position: 12
                speed:
                  unit: "G"
                  value: 10

            # state whether you want to create or delete this resource
            state: present
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_interface_maps

        - debug:
            msg: "{{ cicd_test_interface_maps }}"

        ### #################################################################
        ### # CREATE A NEW RACK TYPE ON APSTRA SERVER
        ### #################################################################
        - name: Create a Rack Type
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical device)
            type: "rack-types"
            label: "cicd_test"
            access_switches: []
            description: cicd_test
            display_name: cicd_test
            id: cicd_test
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
                label: cicd_test
                leaf_leaf_l3_link_port_channel_id: 0
                leaf_leaf_link_port_channel_id: 0
                logical_device: "{{ cicd_test_logical_device['data']['id'] }}"
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
              - display_name: vqfx_leaf
                id: "{{ cicd_test_logical_device['data']['id'] }}"
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
                    target_switch_label: cicd_test
                    lag_mode:
                    leaf_peer:
                    attachment_type: singleAttached
                    label: cicd_test
                label: cicd_test
                logical_device: AOS-1x10-1

            # state whether you want to create or delete this resource
            state: present
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_rack_type

        - debug:
            msg: "{{ cicd_test_rack_type }}"

    ### #################################################################
    ### # DELETE DESIGN PLAY
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
        ### # DELETE A INTERFACE MAPPING ON APSTRA SERVER
        ### #################################################################
        - name: Delete an interface mapping
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical-device)
            type: "interface-maps"
            label: "cicd_test"

            # state whether you want to create or delete this resource
            state: absent
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_interface_maps

        - debug:
            msg: "{{ cicd_test_interface_maps }}"

        ### #################################################################
        ### # DELETE A LOGICAL DEVICE ON APSTRA SERVER
        ### #################################################################
        - name: Delete a logical device
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical-device)
            type: "logical-devices"
            display_name: "cicd_test"

            # state whether you want to create or delete this resource
            state: absent
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_logical_device

        - debug:
            msg: "{{ cicd_test_logical_device }}"

        ### #################################################################
        ### # DELETE A NEW RACK TYPE ON APSTRA SERVER
        ### #################################################################
        - name: Delete a Rack Type
          cdot65.apstra.design:
            # define server connectivity options
            server: apstra.dmz.home
            port: 443
            validate_certs: False
            api_token: "{{ api_token }}"

            # define design element (logical device)
            type: "rack-types"
            id: cicd_test

            # state whether you want to create or delete this resource
            state: absent
          
          # store the output of our task as a new variable to debug later
          register: cicd_test_rack_types

        - debug:
            msg: "{{ cicd_test_rack_types }}"

Example Template File
---------------------

Here is an example import of a Template file

.. code-block:: yaml

    ---
    houston_template:
      asn_allocation_policy:
        spine_asn_scheme: distinct
      dhcp_service_intent:
        active: true
      display_name: houston_template
      external_routing_policy:
        export_policy:
          all_routes: true
          l2edge_subnets: true
          l3edge_server_links: true
          loopbacks: true
          spine_leaf_links: true
        import_policy: default_only
      fabric_addressing_policy:
        spine_leaf_links: ipv4
      rack_type_counts:
        - count: 4
          rack_type_id: houston_rack
      rack_types:
        - access_switches: []
          description: ""
          display_name: houston_rack
          id: houston_rack
          leafs:
            - external_router_facing: false
              external_router_links: []
              label: houston_leaf
              leaf_leaf_l3_link_count: 0
              leaf_leaf_l3_link_port_channel_id: 0
              leaf_leaf_l3_link_speed: null
              leaf_leaf_link_count: 0
              leaf_leaf_link_port_channel_id: 0
              leaf_leaf_link_speed: null
              link_per_spine_count: 1
              link_per_spine_speed:
                unit: G
                value: 10
              logical_device: "{{ logical_device_vqfx_leaf['data']['id'] }}"
              redundancy_protocol: null
          logical_devices:
            - display_name: vqfx_leaf
              id: "{{ logical_device_vqfx_leaf['data']['id'] }}"
              panels:
                - panel_layout:
                    column_count: 12
                    row_count: 1
                  port_groups:
                    - count: 4
                      roles:
                        - spine
                      speed:
                        unit: G
                        value: 10
                    - count: 7
                      roles:
                        - l2_server
                        - access
                        - l3_server
                      speed:
                        unit: G
                        value: 10
                    - count: 1
                      roles:
                        - external_router
                      speed:
                        unit: G
                        value: 10
                  port_indexing:
                    order: T-B, L-R
                    schema: absolute
                    start_index: 1
            - display_name: AOS-1x10-1
              id: AOS-1x10-1
              panels:
                - panel_layout:
                    column_count: 1
                    row_count: 1
                  port_groups:
                    - count: 1
                      roles:
                        - leaf
                        - access
                      speed:
                        unit: G
                        value: 10
                  port_indexing:
                    order: T-B, L-R
                    schema: absolute
                    start_index: 1
          servers:
            - connectivity_type: l2
              count: 1
              ip_version: ipv4
              label: houston_server
              links:
                - attachment_type: singleAttached
                  label: houston_leaf_server
                  lag_mode: null
                  link_per_switch_count: 1
                  link_speed:
                    unit: G
                    value: 10
                  target_switch_label: houston_leaf
              logical_device: AOS-1x10-1
              port_channel_id_max: 0
              port_channel_id_min: 0
      spine:
        count: 2
        external_link_count: 0
        external_link_speed: null
        link_per_superspine_count: 0
        link_per_superspine_speed: null
        logical_device:
          display_name: vqfx_spine
          id: "{{ logical_device_vqfx_spine['data']['id'] }}"
          panels:
            - panel_layout:
                column_count: 12
                row_count: 1
              port_groups:
                - count: 12
                  roles:
                    - leaf
                  speed:
                    unit: G
                    value: 10
              port_indexing:
                order: T-B, L-R
                schema: absolute
                start_index: 1
      type: rack_based
      virtual_network_policy:
        overlay_control_protocol: evpn


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def design_spec():
        return dict(
            access_switches=dict(
                required=False,
                type='list',
                elements='str'
            ),
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback, [
                        'APSTRA_API_TOKEN',
                        'APSTRA_API_TOKEN',
                        'API_TOKEN'
                    ]
                ),
                no_log=True,
                type='str'
            ),
            description=dict(
                required=False,
                type='str'
            ),
            device_profile_id=dict(
                required=False,
                type='str'
            ),
            display_name=dict(
                required=True,
                fallback=(
                    env_fallback, [
                        'APSTRA_USERNAME',
                        'APSTRA_USERNAME',
                        'USERNAME'
                    ]
                ),
                type='str'
            ),
            id=dict(
                required=False,
                type='str'
            ),
            interfaces=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    mapping=dict(
                        required=True,
                        type='list',
                        elements='int'
                    ),
                    name=dict(
                        required=True,
                        type='str',
                    ),
                    position=dict(
                        required=True,
                        type='int',
                    ),
                    roles=dict(
                        required=True,
                        type='list',
                        elements='str'
                    ),
                    setting=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            param=dict(
                                required=False,
                                type='str'
                            ),
                        )
                    ),
                    speed=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            unit=dict(
                                required=False,
                                type='str'
                            ),
                            value=dict(
                                required=False,
                                type='int'
                            ),
                        )
                    ),
                    state=dict(
                        required=True,
                        type='str',
                    ),
                ),
            ),
            label=dict(
                required=False,
                type='str'
            ),
            leafs=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    external_router_facing=dict(
                        required=True,
                        type='bool',
                    ),
                    external_router_links=dict(
                        required=True,
                        type='list',
                        elements='str'
                    ),
                    label=dict(
                        required=False,
                        type='str',
                    ),
                    leaf_leaf_l3_link_count=dict(
                        required=False,
                        type='int',
                    ),
                    leaf_leaf_l3_link_port_channel_id=dict(
                        required=False,
                        type='int',
                    ),
                    leaf_leaf_l3_link_speed=dict(
                        required=False,
                        type='str',
                    ),
                    leaf_leaf_link_count=dict(
                        required=False,
                        type='int',
                    ),
                    leaf_leaf_link_port_channel_id=dict(
                        required=False,
                        type='int',
                    ),
                    leaf_leaf_link_speed=dict(
                        required=False,
                        type='str',
                    ),
                    link_per_spine_count=dict(
                        required=False,
                        type='int',
                    ),
                    link_per_spine_speed=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            unit=dict(
                                required=False,
                                type='str'
                            ),
                            value=dict(
                                required=False,
                                type='int'
                            )
                        )
                    ),
                    logical_device=dict(
                        required=False,
                        type='str',
                    ),
                    redundancy_protocol=dict(
                        required=False,
                        type='str',
                    ),
                ),
            ),
            logical_devices=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    display_name=dict(
                        required=True,
                        type='str',
                    ),
                    id=dict(
                        required=True,
                        type='str',
                    ),
                    panels=dict(
                        required=False,
                        type='list',
                        elements='dict',
                        options=dict(
                            panel_layout=dict(
                                required=True,
                                type='dict',
                                options=dict(
                                    row_count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    column_count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                )
                            ),
                            port_indexing=dict(
                                required=True,
                                type='dict',
                                options=dict(
                                    order=dict(
                                        required=False,
                                        type='str'
                                    ),
                                    start_index=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    schema=dict(
                                        required=False,
                                        type='str'
                                    ),
                                )
                            ),
                            port_groups=dict(
                                required=False,
                                type='list',
                                elements='dict',
                                options=dict(
                                    count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    roles=dict(
                                        required=False,
                                        type='list',
                                        elements='str'
                                    ),
                                    speed=dict(
                                        required=True,
                                        type='dict',
                                        options=dict(
                                            unit=dict(
                                                required=False,
                                                type='str'
                                            ),
                                            value=dict(
                                                required=False,
                                                type='int'
                                            ),
                                        )
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            logical_device_id=dict(
                required=False,
                type='str'
            ),
            name=dict(
                required=False,
                type='str'
            ),
            panels=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    panel_layout=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            row_count=dict(
                                required=False,
                                type='int'
                            ),
                            column_count=dict(
                                required=False,
                                type='int'
                            ),
                        )
                    ),
                    port_indexing=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            order=dict(
                                required=False,
                                type='str'
                            ),
                            schema=dict(
                                required=False,
                                type='str'
                            ),
                            start_index=dict(
                                required=False,
                                type='int'
                            ),
                        ),
                    ),
                    port_groups=dict(
                        required=True,
                        type='list',
                        elements='dict',
                        options=dict(
                            count=dict(
                                required=False,
                                type='int'
                            ),
                            roles=dict(
                                required=False,
                                type='list',
                                elements='str'
                            ),
                            speed=dict(
                                required=False,
                                type='dict',
                                options=dict(
                                    value=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    unit=dict(
                                        required=False,
                                        type='str'
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            port=dict(
                required=False,
                type='int'
            ),
            server=dict(
                required=False,
                type='str'
            ),
            servers=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    connectivity_type=dict(
                        required=True,
                        type='str',
                    ),
                    count=dict(
                        required=True,
                        type='int',
                    ),
                    label=dict(
                        required=True,
                        type='str',
                    ),
                    logical_device=dict(
                        required=True,
                        type='str',
                    ),
                    ip_version=dict(
                        required=True,
                        type='str',
                    ),
                    port_channel_id_min=dict(
                        required=True,
                        type='int',
                    ),
                    port_channel_id_max=dict(
                        required=True,
                        type='int',
                    ),
                    links=dict(
                        required=False,
                        type='list',
                        elements='dict',
                        options=dict(
                            attachment_type=dict(
                                required=False,
                                type='str'
                            ),
                            label=dict(
                                required=False,
                                type='str'
                            ),
                            lag_mode=dict(
                                required=False,
                                type='str'
                            ),
                            leaf_peer=dict(
                                required=False,
                                type='str'
                            ),
                            link_per_switch_count=dict(
                                required=False,
                                type='int'
                            ),
                            link_speed=dict(
                                required=True,
                                type='dict',
                                options=dict(
                                    unit=dict(
                                        required=False,
                                        type='str'
                                    ),
                                    value=dict(
                                        required=False,
                                        type='int'
                                    ),
                                )
                            ),
                            target_switch_label=dict(
                                required=False,
                                type='str'
                            ),
                        ),
                    ),
                ),
            ),
            state=dict(
                required=True,
                choices=[
                    'absent',
                    'present'
                ],
                type='str'
            ),
            design_template=dict(
                required=False,
                type='dict',
                options=dict(
                    asn_allocation_policy=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            spine_asn_scheme=dict(
                                required=False,
                                type='str'
                            )
                        )
                    ),
                    dhcp_service_intent=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            active=dict(
                                required=False,
                                type='bool'
                            )
                        )
                    ),
                    display_name=dict(
                        required=True,
                        type='str'
                    ),
                    external_routing_policy=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            export_policy=dict(
                                required=False,
                                type='dict',
                                options=dict(
                                    all_routes=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                    l2edge_subnets=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                    l3edge_server_links=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                    loopbacks=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                    spine_leaf_links=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                )
                            ),
                            import_policy=dict(
                                required=False,
                                type='str'
                            )
                        )
                    ),
                    fabric_addressing_policy=dict(
                        required=False,
                        type='dict',
                        options=dict(
                            spine_leaf_links=dict(
                                required=False,
                                type='str'
                            )
                        )
                    ),
                    rack_type_counts=dict(
                        required=False,
                        type='list',
                        elements='dict',
                        options=dict(
                            count=dict(
                                required=False,
                                type='int'
                            ),
                            rack_type_id=dict(
                                required=False,
                                type='str'
                            ),
                        )
                    ),
                    rack_types=dict(
                        required=False,
                        type='list',
                        elements='dict',
                        options=dict(
                            access_switches=dict(
                                required=False,
                                type='list',
                                elements='str'
                            ),
                            description=dict(
                                required=False,
                                type='str'
                            ),
                            display_name=dict(
                                required=False,
                                type='str'
                            ),
                            id=dict(
                                required=False,
                                type='str'
                            ),
                            leafs=dict(
                                required=False,
                                type='list',
                                elements='dict',
                                options=dict(
                                    external_router_facing=dict(
                                        required=False,
                                        type='bool'
                                    ),
                                    external_router_links=dict(
                                        required=False,
                                        type='list',
                                        elements='str'
                                    ),
                                    label=dict(
                                        required=False,
                                        type='str'
                                    ),
                                    leaf_leaf_l3_link_count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    leaf_leaf_l3_link_port_channel_id=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    leaf_leaf_l3_link_speed=dict(
                                        required=False,
                                        type='str'
                                    ),
                                    leaf_leaf_link_count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    leaf_leaf_link_port_channel_id=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    leaf_leaf_link_speed=dict(
                                        required=False,
                                        type='str'
                                    ),
                                    link_per_spine_count=dict(
                                        required=False,
                                        type='int'
                                    ),
                                    link_per_spine_speed=dict(
                                        required=False,
                                        type='dict',
                                        options=dict(
                                            unit=dict(
                                                type='str',
                                                required=False
                                            ),
                                            value=dict(
                                                type='int',
                                                required=False
                                            )
                                        )
                                    ),
                                    logical_device=dict(
                                        required=True,
                                        type='str'
                                    ),
                                    redundancy_protocol=dict(
                                        required=False,
                                        type='str'
                                    ),
                                )
                            ),
                            logical_devices=dict(
                                required=False,
                                type='list',
                                elements='dict',
                                options=dict(
                                    display_name=dict(
                                        required=True,
                                        type='str'
                                    ),
                                    id=dict(
                                        required=True,
                                        type='str'
                                    ),
                                    panels=dict(
                                        required=False,
                                        type='list',
                                        elements='dict',
                                        options=dict(
                                            panel_layout=dict(
                                                required=False,
                                                type='dict',
                                                options=dict(
                                                    column_count=dict(
                                                        required=False,
                                                        type='int'
                                                    ),
                                                    row_count=dict(
                                                        required=False,
                                                        type='int'
                                                    )
                                                )
                                            ),
                                            port_groups=dict(
                                                required=False,
                                                type='list',
                                                elements='dict',
                                                options=dict(
                                                    count=dict(
                                                        required=False,
                                                        type='int'
                                                    ),
                                                    roles=dict(
                                                        required=False,
                                                        type='list',
                                                        elements='str'
                                                    ),
                                                    speed=dict(
                                                        required=False,
                                                        type='dict',
                                                        options=dict(
                                                            unit=dict(
                                                                required=False,
                                                                type='str'
                                                            ),
                                                            value=dict(
                                                                required=False,
                                                                type='int'
                                                            ),
                                                        )
                                                    ),
                                                )
                                            ),
                                            port_indexing=dict(
                                                required=True,
                                                type='dict',
                                                options=dict(
                                                    order=dict(
                                                        required=True,
                                                        type='str'
                                                    ),
                                                    schema=dict(
                                                        required=True,
                                                        type='str'
                                                    ),
                                                    start_index=dict(
                                                        required=True,
                                                        type='int'
                                                    ),
                                                )
                                            )
                                        )
                                    )
                                )
                            ),
                            servers=dict(
                                required=True,
                                type='list',
                                elements='dict',
                                options=dict(
                                    connectivity_type=dict(
                                        type='str',
                                        required=True
                                    ),
                                    count=dict(
                                        type='int',
                                        required=True
                                    ),
                                    ip_version=dict(
                                        type='str',
                                        required=True
                                    ),
                                    label=dict(
                                        type='str',
                                        required=True
                                    ),
                                    links=dict(
                                        required=True,
                                        type='list',
                                        elements='dict',
                                        options=dict(
                                            attachment_type=dict(
                                                type='str',
                                                required=True
                                            ),
                                            label=dict(
                                                type='str',
                                                required=True
                                            ),
                                            lag_mode=dict(
                                                type='str',
                                                required=False
                                            ),
                                            link_per_switch_count=dict(
                                                type='int',
                                                required=False
                                            ),
                                            link_speed=dict(
                                                required=True,
                                                type='dict',
                                                options=dict(
                                                    unit=dict(
                                                        type='str',
                                                        required=False
                                                    ),
                                                    value=dict(
                                                        type='int',
                                                        required=False
                                                    )
                                                )
                                            ),
                                            target_switch_label=dict(
                                                type='str',
                                                required=True
                                            )
                                        )
                                    ),
                                    logical_device=dict(
                                        type='str',
                                        required=True
                                    ),
                                    port_channel_id_max=dict(
                                        type='int',
                                        required=False
                                    ),
                                    port_channel_id_min=dict(
                                        type='int',
                                        required=False
                                    )
                                )
                            )
                        )
                    ),
                    spine=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            count=dict(
                                required=True,
                                type='int'
                            ),
                            external_link_count=dict(
                                required=True,
                                type='int'
                            ),
                            external_link_speed=dict(
                                required=True,
                                type='str'
                            ),
                            link_per_superspine_count=dict(
                                required=True,
                                type='int'
                            ),
                            link_per_superspine_speed=dict(
                                required=True,
                                type='str'
                            ),
                            logical_device=dict(
                                required=True,
                                type='dict',
                                options=dict(
                                    display_name=dict(
                                        required=True,
                                        type='str'
                                    ),
                                    id=dict(
                                        required=True,
                                        type='str'
                                    ),
                                    panels=dict(
                                        required=False,
                                        type='list',
                                        elements='dict',
                                        options=dict(
                                            panel_layout=dict(
                                                required=False,
                                                type='dict',
                                                options=dict(
                                                    column_count=dict(
                                                        required=False,
                                                        type='int'
                                                    ),
                                                    row_count=dict(
                                                        required=False,
                                                        type='int'
                                                    )
                                                )
                                            ),
                                            port_groups=dict(
                                                required=False,
                                                type='list',
                                                elements='dict',
                                                options=dict(
                                                    count=dict(
                                                        required=False,
                                                        type='int'
                                                    ),
                                                    roles=dict(
                                                        required=False,
                                                        type='list',
                                                        elements='str'
                                                    ),
                                                    speed=dict(
                                                        required=False,
                                                        type='dict',
                                                        options=dict(
                                                            unit=dict(
                                                                required=False,
                                                                type='str'
                                                            ),
                                                            value=dict(
                                                                required=False,
                                                                type='int'
                                                            )
                                                        )
                                                    )
                                                )
                                            ),
                                            port_indexing=dict(
                                                required=False,
                                                type='dict',
                                                options=dict(
                                                    order=dict(
                                                        type='str',
                                                        required=False
                                                    ),
                                                    schema=dict(
                                                        type='str',
                                                        required=False
                                                    ),
                                                    start_index=dict(
                                                        type='int',
                                                        required=False
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    type=dict(
                        required=True,
                        type='str'
                    ),
                    virtual_network_policy=dict(
                        required=True,
                        type='dict',
                        options=dict(
                            overlay_control_protocol=dict(
                                required=True,
                                type='str'
                            )
                        )
                    )
                )
            ),
            type=dict(
                required=True,
                choices=[
                    'logical-devices',
                    'interface-maps',
                    'rack-types',
                    'templates'
                ],
                type='str'
            ),
            validate_certs=dict(
                type='bool',
                required=False,
                default=False
            ),
        )
