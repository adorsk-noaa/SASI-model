import os
basedir = os.path.dirname(os.path.abspath(__file__))

conf = {
	'verbose': True,
    'dry_code_to_gear_category':  {
        'GC1': 'Trawl',
        'GC2': 'Scallop',
        'GC3': 'Dredge',
        'GC4': 'Longline',
        'Gillnet': 'GC5',
        'Trap': 'GC6'
    },
    'results_georefine_schema': os.path.join(basedir, "templates", "georefine", "results_schema.py"),
    'results_georefine_app_config': os.path.join(basedir, "templates", "georefine", "results_app_config.py"),
}

import secrets
conf.update(secrets.secrets)
