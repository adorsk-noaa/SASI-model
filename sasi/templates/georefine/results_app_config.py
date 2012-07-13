filter_groups = [
        {'id': 'scenario'},
        {'id': 'data'}
        ]

facet_quantity_fields = [
        {
            'id': 'Result.cell.area:sum',
            'label': 'Cell Area (km^2): sum',
            'value_type': 'numeric',
            'entity': {
                'expression': 'func.sum({Result.cell.area})/1000000',
                'format': '%.1e km^2'
                }
            },
        {
            'id': 'Result.cell.id:count',
            'label': 'Number of relevant cells',
            'value_type': 'numeric',
            'entity': {
                'expression': 'func.count({Result.cell.id})',
                'format': '%s cells'
                }
            }
        ]

facets = [
        {
            'id': 'timestep',
            'label': 'Timestep',
            'type': 'time-slider',
            'grouping_entity': {
                'expression': '{Result.t}'
                },
            'sorting_entity': {
                'expression': '{Result.t}',
                'direction': 'asc'
                },
            'value_type': 'numeric',
            'choices': [],
            'filter_groups': ['scenario']
            },
        {
            'id': 'substrate',
            'label': 'Substrates',
            'type': 'list',
            'grouping_entity': {
                'expression': '{Result.substrate.id}',
                'label_entity': {
                    'expression': '{Result.substrate.name}'
                    }
                },
            'count_entity': {
                'expression': 'func.sum({Result.cell.area})/(1000000)',
                'format': '%.1e km^2'
                },
            'filter_groups': ['data'],
            'base_filter_groups': ['scenario'],
            },
        ]

charts = {
        'filter_groups': ['data'],
        'base_filter_groups': ['scenario'],
        'category_fields': [
            {
                'id': 'substrates',
                'entity': {
                    'expression': '{Result.substrate.name}',
                    'all_values': True,
                    },
                'label': 'Substrates',
                'value_type': 'categorical',
                },
            ],

        'quantity_fields' : [
            {
                'id': 'Result.cell.area:sum',
                'label': 'Cell Area (km^2): sum',
                'value_type': 'numeric',
                'entity': {
                    'expression': 'func.sum({Result.cell.area})/1000000',
                    'min': 0,
                    'maxauto': 'true',
                    }
                }
            ]
        }

map = {
        'filter_groups': ['data'],
        "max_extent" : [-79, 31, -65, 45],
        "graticule_intervals": [2],
        "resolutions": [0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125],
        "default_layer_options" : {
            "transitionEffect": 'resize'
            },
        "default_layer_attributes": {
            "disabled": True
            },

        "base_filter_groups" : ['scenario'],
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
                "data_entity": {
                    "expression": "func.sum({Result.x}/{Result.cell.area})",
                    "label": "x",
                    "min": 0,
                    "max": .25,
                    },
                "grouping_entities": [
                    ],
                "geom_entity": {
                    "expression": "{Result.cell.geom}.RAW",
                    },
                "geom_id_entity": {
                    "expression": "{Result.cell.id}"
                    },
                "filters": [],
                "disabled": False
                }
            ],
        "base_layers": [
            ],
        "overlay_layers": [
            ]
        }

summary_bar = {
        "quantity_fields": [
            {
                'id': 'Result.cell.area:sum',
                'label': 'Cell Area (km^2): sum',
                'entity': {
                    'expression': 'func.sum({Result.cell.area})/1000000'
                    },
                'format': '%.1e km^2'
                },
            ],
        'filter_groups': ['data'],
        'base_filter_groups': ['scenario']
        }

initial_state = {
        "summary_bar": {
            "selected": "Result.cell.area:sum"
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
                    'id': 'Result.cell.area:sum',
                    }
                },
            ]
        }

