conf = {
	'verbose': True,
    'dry_code_to_gear_category':  {
        'GC1': 'Trawl',
        'GC2': 'Scallop',
        'GC3': 'Dredge',
        'GC4': 'Longline',
        'Gillnet': 'GC5',
        'Trap': 'GC6'
    }
}

import secrets
conf.update(secrets.secrets)
