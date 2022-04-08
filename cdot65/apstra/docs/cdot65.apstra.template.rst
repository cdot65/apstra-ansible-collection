======================
cdot65.apstra.template
======================

---------------------
Manage your Templates
---------------------

template
========

This module will allow you to manage your Design Templates within Apstra.

Feature set as of version 0.0.11:
  - manage Design Templates
  - idempotent

Example
-------

Here is a basic example of using the module to mange your resources in Apstra

.. code-block:: yaml

    ### #################################################################
    ### # CREATE TEMPLATE FOR OUR BLUEPRINT
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



Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def design_template_spec():
        """Defined the data model for creating a new design template."""
        return dict(
            api_token=dict(
                required=True,
                fallback=(
                    env_fallback,
                    ["APSTRA_API_TOKEN", "APSTRA_API_TOKEN", "API_TOKEN"],
                ),
                no_log=True,
                type="str",
            ),
            description=dict(required=False, type="str"),
            dhcp_service_intent=dict(required=False, type="dict", options=dict(
                active=dict(required=False, type="str"))),
            display_name=dict(
                required=True,
                type="str",
            ),
            id=dict(required=False, type="str"),
            mesh_link_speed=dict(
                required=False,
                type="dict",
                options=dict(
                    unit=dict(required=False, type="str"),
                    value=dict(required=False, type="int"),
                ),
            ),
            mesh_link_count=dict(required=False, type="int"),
            port=dict(required=False, type="int"),
            rack_type_counts=dict(
                required=True,
                type="list",
                elements="dict",
                options=dict(
                    count=dict(
                        required=True,
                        type="int",
                    ),
                    rack_type_id=dict(
                        required=True,
                        type="str",
                    ),
                ),
            ),
            rack_types=dict(
                required=True,
                type="list",
                elements="dict",
                options=dict(
                    access_switches=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            access_access_link_count=dict(
                                required=True,
                                type="int",
                            ),
                            access_access_link_speed=dict(
                                required=False,
                                type="dict",
                                options=dict(
                                    unit=dict(
                                        required=True,
                                        type="str",
                                    ),
                                    value=dict(
                                        required=True,
                                        type="int",
                                    ),
                                ),
                            ),
                            instance_count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    lag_mode=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    link_per_switch_count=dict(
                                        required=False, type="int"),
                                    link_speed=dict(
                                        required=False,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=True,
                                                type="str",
                                            ),
                                            value=dict(
                                                required=True,
                                                type="int",
                                            ),
                                        ),
                                    ),
                                    tags=dict(required=True, type="list",
                                              elements="str"),
                                    target_switch_label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            redundancy_protocol=dict(
                                required=True,
                                type="str",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    description=dict(required=False, type="str"),
                    display_name=dict(
                        required=False,
                        type="str",
                    ),
                    fabric_connectivity_design=dict(required=True, type="str"),
                    generic_systems=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            asn_domain=dict(
                                required=True,
                                type="str",
                            ),
                            count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    lag_mode=dict(
                                        required=False,
                                        type="str",
                                    ),
                                    link_per_switch_count=dict(
                                        required=False,
                                        type="int",
                                    ),
                                    link_speed=dict(
                                        required=False,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=True,
                                                type="str",
                                            ),
                                            value=dict(
                                                required=True,
                                                type="int",
                                            ),
                                        ),
                                    ),
                                    switch_peer=dict(
                                        required=False, type="str"),
                                    tags=dict(required=True, type="list",
                                              elements="str"),
                                    target_switch_label=dict(
                                        required=False,
                                        type="str",
                                    ),
                                ),
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            loopback=dict(
                                required=True,
                                type="str",
                            ),
                            management_level=dict(
                                required=True,
                                type="str",
                            ),
                            port_channel_id_max=dict(
                                required=True,
                                type="int",
                            ),
                            port_channel_id_min=dict(
                                required=True,
                                type="int",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    id=dict(required=False, type="str"),
                    leafs=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            label=dict(
                                required=False,
                                type="str",
                            ),
                            leaf_leaf_l3_link_count=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_l3_link_port_channel_id=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_l3_link_speed=dict(
                                required=False,
                                type="str",
                            ),
                            leaf_leaf_link_count=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_link_port_channel_id=dict(
                                required=False,
                                type="int",
                            ),
                            leaf_leaf_link_speed=dict(
                                required=False,
                                type="str",
                            ),
                            link_per_spine_count=dict(
                                required=False,
                                type="int",
                            ),
                            logical_device=dict(
                                required=False,
                                type="str",
                            ),
                            redundancy_protocol=dict(
                                required=False,
                                type="str",
                            ),
                            tags=dict(required=True, type="list",
                                      elements="str"),
                        ),
                    ),
                    logical_devices=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            display_name=dict(
                                required=True,
                                type="str",
                            ),
                            id=dict(
                                required=True,
                                type="str",
                            ),
                            panels=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    panel_layout=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            row_count=dict(
                                                required=False, type="int"),
                                            column_count=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                    port_indexing=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            order=dict(
                                                required=False, type="str"),
                                            start_index=dict(
                                                required=False, type="int"),
                                            schema=dict(
                                                required=False, type="str"),
                                        ),
                                    ),
                                    port_groups=dict(
                                        required=False,
                                        type="list",
                                        elements="dict",
                                        options=dict(
                                            count=dict(
                                                required=False, type="int"),
                                            roles=dict(required=False,
                                                       type="list", elements="str"),
                                            speed=dict(
                                                required=True,
                                                type="dict",
                                                options=dict(
                                                    unit=dict(
                                                        required=False, type="str"),
                                                    value=dict(
                                                        required=False, type="int"),
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                    servers=dict(
                        required=False,
                        type="list",
                        elements="dict",
                        options=dict(
                            connectivity_type=dict(
                                required=True,
                                type="str",
                            ),
                            count=dict(
                                required=True,
                                type="int",
                            ),
                            label=dict(
                                required=True,
                                type="str",
                            ),
                            logical_device=dict(
                                required=True,
                                type="str",
                            ),
                            ip_version=dict(
                                required=True,
                                type="str",
                            ),
                            port_channel_id_min=dict(
                                required=True,
                                type="int",
                            ),
                            port_channel_id_max=dict(
                                required=True,
                                type="int",
                            ),
                            links=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    attachment_type=dict(
                                        required=False, type="str"),
                                    label=dict(required=False, type="str"),
                                    lag_mode=dict(required=False, type="str"),
                                    leaf_peer=dict(required=False, type="str"),
                                    link_per_switch_count=dict(
                                        required=False, type="int"),
                                    link_speed=dict(
                                        required=True,
                                        type="dict",
                                        options=dict(
                                            unit=dict(
                                                required=False, type="str"),
                                            value=dict(
                                                required=False, type="int"),
                                        ),
                                    ),
                                    target_switch_label=dict(
                                        required=False, type="str"),
                                ),
                            ),
                        ),
                    ),
                    tags=dict(
                        required=False,
                        type="list",
                        elements="str",
                    ),
                ),
            ),
            type=dict(required=True, type="str"),
            virtual_network_policy=dict(
                required=True,
                type="dict",
                options=dict(
                    overlay_control_protocol=dict(required=True, type="str"),
                ),
            ),
            server=dict(required=False, type="str"),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            tags=dict(
                required=False,
                type="list",
                elements="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )
