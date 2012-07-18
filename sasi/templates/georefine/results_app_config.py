filter_groups = [
        {'id': 'scenario'},
        {'id': 'data'}
        ]

facets = {
        "quantity_fields": [
            {
                'id': 'result.cell.area:sum',
                'label': 'Cell Area (km^2): sum',
                'value_type': 'numeric',
                'inner_query': {
                    'SELECT': [{'ID': 'cell_area', 'EXPRESSION': '{{result.cell.area}}/1000000.0'}],
                    'GROUP_BY': [
                        '{{result.cell.id}}',
                        {'ID': 'cell_area'}
                        ],
                    },
                'outer_query': {
                    'SELECT': [{'ID': 'sum_cell_area', 'EXPRESSION': 'func.sum({{inner.cell_area}})'}],
                    },
                'format': '%.1e km<sup>2</sup>'
                },
            {
                'id': 'result.cell.id:count',
                'label': 'Number of relevant cells',
                'value_type': 'numeric',
                'inner_query': {
                    'SELECT': [{'ID': 'cell_id', 'EXPRESSION': '{{result.cell.id}}'}],
                    'GROUP_BY': [{'ID': 'cell_id'}],
                    },
                'outer_query': {
                    'SELECT': [{'ID': 'count_cell_id', 'EXPRESSION': 'func.count({{inner.cell_id}})'}],
                    },
                'format': '%s cells'
                }
            ],

        "facets" : [
            {
                'id': 'timestep',
                'label': 'Timestep',
                'type': 'time-slider',
                'KEY': {
                    'KEY_ENTITY': {'ID': 'result_t', 'EXPRESSION': '{{result.t}}'},
                    'LABEL_ENTITY': {'ID': 'result_t'},
                    },
                'value_type': 'numeric',
                'choices': [],
                'primary_filter_groups': ['scenario'],
                'filter_entity': '{{result.t}}',
                },
            {
                'id': 'substrates',
                'label': 'Substrates',
                'type': 'list',
                'KEY': {
                    'KEY_ENTITY': {'ID': 'substrate_id', 'EXPRESSION': '{{result.substrate.id}}'},
                    'LABEL_ENTITY': {'ID': 'substrate_name', 'EXPRESSION': '{{result.substrate.name}}'},
                    },
                'primary_filter_groups': ['data'],
                'base_filter_groups': ['scenario'],
                'filter_entity': '{{result.substrate.id}}'
                },
            {
                'id': 'x',
                'label': 'Numeric Test',
                'type': 'numeric',
                'KEY': {
                    'KEY_ENTITY': {
                        'ID': 'x', 
                        'EXPRESSION': '{{result.x}}',
                        'AS_HISTOGRAM': True,
                        'ALL_VALUES': True
                        },
                    },
                'primary_filter_groups': ['data'],
                'base_filter_groups': ['scenario'],
                'filter_entity': '{{result.x}}',
                'range_auto': True
                },
            ]
        }

charts = {
        'primary_filter_groups': ['data'],

        'base_filter_groups': ['scenario'],

        'category_fields': [
            {
                'id': 'x',
                'label': 'X Test',
                'value_type': 'numeric',
                'KEY': {
                    'KEY_ENTITY': {
                        'ID': 'x', 
                        'EXPRESSION': '{{result.x}}',
                        'AS_HISTOGRAM': True,
                        'ALL_VALUES': True
                        },
                    },
                },
            {
                'id': 'substrates',
                'label': 'Substrates',
                'value_type': 'categorical',
                'KEY': {
                    'KEY_ENTITY': {
                        'ID': 'substrate_id', 
                        'EXPRESSION': '{{result.substrate.id}}',
                        'ALL_VALUES': True
                        },
                    'LABEL_ENTITY': {'ID': 'substrate_name', 'EXPRESSION': '{{result.substrate.name}}'},
                    },
                },
            ],

        'quantity_fields': [
            {
                'id': 'result.cell.area:sum',
                'label': 'Cell Area (km^2): sum',
                'value_type': 'numeric',
                'inner_query': {
                    'SELECT': [{'ID': 'cell_area', 'EXPRESSION': '{{result.cell.area}}/1000000.0'}],
                    'GROUP_BY': [
                        '{{result.cell.id}}',
                        {'ID': 'cell_area'}
                        ],
                    },
                'outer_query': {
                    'SELECT': [{'ID': 'sum_cell_area', 'EXPRESSION': 'func.sum({{inner.cell_area}})'}],
                    },
                'format': '%.1e km<sup>2</sup>'
                },
            {
                'id': 'result.cell.id:count',
                'label': 'Number of relevant cells',
                'value_type': 'numeric',
                'inner_query': {
                    'SELECT': [{'ID': 'cell_id', 'EXPRESSION': '{{result.cell.id}}'}],
                    'GROUP_BY': [{'ID': 'cell_id'}],
                    },
                'outer_query': {
                    'SELECT': [{'ID': 'count_cell_id', 'EXPRESSION': 'func.count({{inner.cell_id}})'}],
                    },
                'format': '%s cells'
                }
            ]
        }


maps = {
        "primary_filter_groups": ['data'],
        "base_filter_groups" : ['scenario'],
        "max_extent" : [-79, 31, -65, 45],
        "graticule_intervals": [2],
        "resolutions": [0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125],
        "default_layer_options" : {
            "transitionEffect": 'resize'
            },
        "default_layer_attributes": {
            "disabled": True
            },

        "data_layers" : [
            {
                "id": "x",
                "name": "X",
                "source": "local_getmap",
                "layer_type": 'WMS',
                "layer_category": 'data',
                "options": {},
                "params": {
                    "transparent": True
                    },
                "inner_query": {
                    'SELECT': [
                        {'ID': 'data', 'EXPRESSION': 'func.sum({{result.x}}/{{result.cell.area}})'},
                        ],
                    'GROUP_BY': [
                        {'ID': 'cell_id', 'EXPRESSION': '{{result.cell.id}}'},
                        {'ID': 'cell_geom', 'EXPRESSION': 'RawColumn({{result.cell.geom}})'}
                        ],
                    },
                "outer_query": {
                    'SELECT': [
                        {'ID': 'geom_id', 'EXPRESSION': '{{inner.cell_id}}'},
                        {'ID': 'geom', 'EXPRESSION': 'RawColumn({{inner.cell_geom}})'},
                        {'ID': 'data', 'EXPRESSION': '{{inner.data}}'},
                        ]
                    },
                "geom_id_entity": {'ID': 'geom_id'},
                "geom_entity": {'ID': 'geom'},
                "data_entity": {
                    'ID': 'data',
                    'min': 0,
                    'max': .25,
                    },
                "disabled": False
                }
            ],

        "base_layers": [
            ],

        "overlay_layers": [
            ]
        }

summary_bar = {
       'primary_filter_groups': ['data'],
        'base_filter_groups': ['scenario']
        }

initial_state = {
        "facets": {
            "initial_quantity_field_id": 'result.cell.area:sum',
            },

        "data_views": [
            {
                "type": "map",
                },
            {
                "type": "chart",
                "initial_category_field": {
                    'id': 'substrates',
                    },
                "initial_quantity_field": {
                    'id': 'result.cell.id:count',
                    }
                },
            ]
        }

