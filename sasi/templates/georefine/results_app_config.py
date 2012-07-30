sasipedia_base_url = "/georefine/static/sasipedia"

quantity_fields = {
    'result.cell.area:sum': { 
        'id': 'result.cell.area:sum',
        'label': 'Cell Area',
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
        'format': '%.1h km<sup>2</sup>'
        },
}

# Add SASI swept area fields to quantity fields.
sasi_fields = [
        ['a', 'Unmodified Swept Area (A)', 0],
        ['y', 'Modified Swept Area (Y)'],
        ['x', 'Recovered Swept Area (X)'],
        ['z', 'Net Swept Area (Z)'],
        ['znet', 'Cumulative Net Swept Area (Znet)'],
        ]

for f in sasi_fields:
    field_id = "result.%s:sum" % f[0]
    quantity_fields[field_id] = {
            'id': field_id,
            'label': f[1],
            'value_type': 'numeric',
            'inner_query': {
                'GROUP_BY': [
                    {'ID': f[0], 'EXPRESSION': "{{result.%s}}/1000000.0" % f[0]},
                    '{{result.id}}'
                    ],
                },
            'outer_query': {
                'SELECT': [{'ID': "%s_sum" % f[0], 'EXPRESSION': "func.sum({{inner.%s}})" % f[0]}],
                },
            'format': '%.1h km<sup>2</sup>'
            }

filter_groups = [
        {'id': 'scenario'},
        {'id': 'data'}
        ]

facets = {
        "quantity_fields": quantity_fields.values(),
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
                'info': 'Info test',
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
                        'ID': 'facetx_x', 
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

        'quantity_fields': quantity_fields.values(),

        }

data_layers = []
for f in sasi_fields:
    data_layer = {
            "id": f[0],
            "name": "%s (density)" % f[1],
            "info": "info test",
            "source": "local_getmap",
            "layer_type": 'WMS',
            "layer_category": 'data',
            "options": {},
            "params": {
                "transparent": True
                },
            "inner_query": {
                'SELECT': [
                    {
                        'ID': "%s_data" % f[0], 
                        'EXPRESSION': "func.sum({{result.%s}}/{{result.cell.area}})" % f[0]
                        },
                    ],
                'GROUP_BY': [
                    {
                        'ID': "%s_cell_id" % f[0], 
                        'EXPRESSION': '{{result.cell.id}}'
                        },
                    {
                        'ID': "%s_cell_geom" % f[0], 
                        'EXPRESSION': 'RawColumn({{result.cell.geom}})'
                        }
                    ],
                },
            "outer_query": {
                'SELECT': [
                    {
                        'ID': "%s_geom_id" % f[0], 
                        'EXPRESSION': "{{inner.%s_cell_id}}" % f[0]
                        },
                    {
                        'ID': "%s_geom" % f[0], 
                        'EXPRESSION': "RawColumn({{inner.%s_cell_geom}})" % f[0]
                        },
                    {
                        'ID': "%s_data" % f[0], 
                        'EXPRESSION': "{{inner.%s_data}}" % f[0]
                        },
                    ]
                },
            "geom_id_entity": {'ID': "%s_geom_id" % f[0]},
            "geom_entity": {'ID': "%s_geom" % f[0]},
            "data_entity": {
                'ID': "%s_data" % f[0],
                'min': 0,
                'max': .25,
                },
            "disabled": True 
            }
    data_layers.append(data_layer)

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
            "reorderable": True,
            "disabled": True
            },

        "data_layers": data_layers,
        #"data_layers" : [
            #{
                #"id": "x",
                #"name": "Recovery (density)",
                #"source": "local_getmap",
                #"layer_type": 'WMS',
                #"layer_category": 'data',
                #"options": {},
                #"params": {
                    #"transparent": True
                    #},
                #"inner_query": {
                    #'SELECT': [
                        #{'ID': 'x_data', 'EXPRESSION': 'func.sum({{result.x}}/{{result.cell.area}})'},
                        #],
                    #'GROUP_BY': [
                        #{'ID': 'x_cell_id', 'EXPRESSION': '{{result.cell.id}}'},
                        #{'ID': 'x_cell_geom', 'EXPRESSION': 'RawColumn({{result.cell.geom}})'}
                        #],
                    #},
                #"outer_query": {
                    #'SELECT': [
                        #{'ID': 'x_geom_id', 'EXPRESSION': '{{inner.x_cell_id}}'},
                        #{'ID': 'x_geom', 'EXPRESSION': 'RawColumn({{inner.x_cell_geom}})'},
                        #{'ID': 'x_data', 'EXPRESSION': '{{inner.x_data}}'},
                        #]
                    #},
                #"geom_id_entity": {'ID': 'x_geom_id'},
                #"geom_entity": {'ID': 'x_geom'},
                #"data_entity": {
                    #'ID': 'x_data',
                    #'min': 0,
                    #'max': .25,
                    #},
                #"disabled": False
                #}
            #],

        "base_layers": [
                {
                    "id":"sasi:world_borders",
                    "name":"Coastal Outlines",
                    "layer_category":"base",
                    "source":"local_geoserver",
                    "workspace":"sasi",
                    "disabled": False,
                    "max_extent":"-180,-90,180,90",
                    "params":{
                        "transparent": False,
                        "layers":"sasi:world_borders",
                         "bgcolor": '0xDEF5FF'
                        },
                    "layer_type":"WMS",
                    "options":{},
                    },
            ],

        "overlay_layers": [
                {
                    "id":"topp:states",
                    "name":"State Bounds",
                    "layer_category":"overlay",
                    "source":"local_geoserver",
                    "workspace":"topp",
                    "disabled": False,
                    "max_extent":"-180,-90,180,90",
                    "params":{
                        "transparent": True,
                        "layers":"topp:states",
                        "styles": "sasi_state_bounds"
                        },
                    "layer_type":"WMS",
                    "options":{},
                    },
                {
                    "id":"sasi:useez",
                    "name":"US EEZ",
                    "layer_category":"overlay",
                    "source":"local_geoserver",
                    "workspace":"sasi",
                    "disabled": False,
                    "max_extent":"-180,-90,180,90",
                    "params":{
                        "transparent": True,
                        "layers":"sasi:useez",
                        "styles": "sasi_useez"
                        },
                    "layer_type":"WMS",
                    "options":{},
                    },
                {
                    "id":"sasi:bathymetry_contours",
                    "name":"Bathymetry Contours",
                    "layer_category":"overlay",
                    "source":"local_geoserver",
                    "workspace":"sasi",
                    "disabled": True,
                    "max_extent":"-180,-90,180,90",
                    "params":{
                        "transparent": True,
                        "layers":"sasi:bathymetry_contours",
                        "styles": "sasi_bathymetry_contours"
                        },
                    "layer_type":"WMS",
                    "options":{},
                    }
            ]
        }

summary_bar = {
       'primary_filter_groups': ['data'],
        'base_filter_groups': ['scenario']
        }

initial_state = {
        "facet_quantity_field": 'result.cell.area:sum',
        "facets": {
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
                    'id': 'result.cell.area:sum',
                    }
                },
            ]
        }

