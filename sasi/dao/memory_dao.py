"""
This class provides an interface to data stored in memory.
"""

class Memory_DAO(object):
    def __init__(self, items=[]):
        self.items = items

    def all(self):
        return self.items

    def query(self, filters=[]):
        results = []

        for item in self.items:
            passes = True

            # Assumes filters are like: {'entity': {'expression': '{prop}'}, 'op': '==', 'value': 'foo'}.
            for f in filters:
                entity = f['entity']
                expression = entity['expression']
                entity_code = re.sub('{(.*?)}', r'getattr(item, "\1")', entity['expression'])
                filter_code = "%s %s %s" % (entity_code, f['op'], f['value'])
                if not eval(filter_code):
                    passes = False
                    break

            if passes:
                results.append(item)

        return results

