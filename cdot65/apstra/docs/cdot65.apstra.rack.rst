==================
cdot65.apstra.rack
==================

----------------------
Manage your Rack Types
----------------------

rack
====

This module will allow you to manage your Rack Types within Apstra.

Feature set as of version 0.0.11:
  - manage rack types
  - idempotent

Example
-------

Here is a basic example of using the module to mange your rack types in Apstra

.. code-block:: yaml

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


Data Model
----------

If you'd like to see the options available for you within the module, have a look at the data model provided below. 

.. code-block:: python

    @staticmethod
    def rack_spec():
        """Defined the data model for creating a new rack type."""
        return dict(
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
                    tags=dict(required=True, type="list", elements="str"),
                ),
            ),
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
                            switch_peer=dict(required=False, type="str"),
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
                    tags=dict(required=True, type="list", elements="str"),
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
                    tags=dict(required=True, type="list", elements="str"),
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
                                    row_count=dict(required=False, type="int"),
                                    column_count=dict(
                                        required=False, type="int"),
                                ),
                            ),
                            port_indexing=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    order=dict(required=False, type="str"),
                                    start_index=dict(
                                        required=False, type="int"),
                                    schema=dict(required=False, type="str"),
                                ),
                            ),
                            port_groups=dict(
                                required=False,
                                type="list",
                                elements="dict",
                                options=dict(
                                    count=dict(required=False, type="int"),
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
            port=dict(required=False, type="int"),
            server=dict(required=False, type="str"),
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
                            attachment_type=dict(required=False, type="str"),
                            label=dict(required=False, type="str"),
                            lag_mode=dict(required=False, type="str"),
                            leaf_peer=dict(required=False, type="str"),
                            link_per_switch_count=dict(
                                required=False, type="int"),
                            link_speed=dict(
                                required=True,
                                type="dict",
                                options=dict(
                                    unit=dict(required=False, type="str"),
                                    value=dict(required=False, type="int"),
                                ),
                            ),
                            target_switch_label=dict(
                                required=False, type="str"),
                        ),
                    ),
                ),
            ),
            state=dict(required=True, choices=[
                       "absent", "present"], type="str"),
            tags=dict(
                required=False,
                type="list",
                elements="str",
            ),
            validate_certs=dict(type="bool", required=False, default=False),
        )
