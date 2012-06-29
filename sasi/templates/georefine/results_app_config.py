facets = [
        {
			'id': 'substrate',
			'label': 'Substrates',
			'type': 'list',
			'grouping_entity': {
				'expression': '{Result.substrate.name}'
				},
			'count_entity': {
				'expression': 'func.sum({Result.cell.area})'
				},
			},
		]

charts = {
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
                'label': 'Cell Area: sum',
				'value_type': 'numeric',
				'entity': {
					'expression': 'func.sum({Result.cell.area})',
					'min': 0,
					'maxauto': 'true',
					}
				}
			]
		}

map = {
		"max_extent" : [-79, 31, -65, 45],
		"graticule_intervals": [2],
		"resolutions": [0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125],
		"default_layer_options" : {
			"transitionEffect": 'resize'
			},
		"default_layer_attributes": {
			"disabled": True
			},

		"base_filters" : [],
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
					"max": 1,
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
                'label': 'Cell Area: sum',
				'entity': {
					'expression': 'func.sum({Result.cell.area})'
					}
				},
			]
		}
		
initial_state = {
		"summary_bar": {
            "selected": "Result.cell.area:sum"
			},

		"data_views": [
			{
				"type": "map",
                },
            ]
        }

