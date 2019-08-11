import json


class CORS(object):
    _options = {
        'origin': '*',
        'origins': [],
        'allow_headers': None,
        'expose_headers': None,
        'credentials': False
    }

    def __init__(self, options={}):
        self._options.update(options)

    def get_origin(self, state):
        state['event']['headers'] = state['event'].get('headers', {})

        if self._options['origins'] and len(self._options['origins']):
            if state['event']['headers'].get('Origin') and state['event']['headers']['Origin'] in self._options['origins']:
                return state['event']['headers']['Origin']
            else:
                return self._options['origins'][0]
        else:
            if state['event']['headers'].get('Origin') and self._options['credentials'] and self._options['origin'] == '*':
                return state['event']['headers']['Origin']
            return self._options['origin']

    def add_cors_headers(self, state):
        if state['event'].get('httpMethod') == None:
            return

        state['response'] = state.get('response', {})
        state['response']['headers'] = state['response'].get('headers', {})

        # Check if already setup Access-Control-Allow-Headers
        if self._options['allow_headers'] and not state['response']['headers'].get('Access-Control-Allow-Headers'):
            state['response']['headers']['Access-Control-Allow-Headers'] = self._options['allow_headers']

        # Check if already setup Access-Control-Expose-Headers
        if self._options['allow_headers'] and not state['response']['headers'].get('Access-Control-Expose-Headers'):
            state['response']['headers']['Access-Control-Expose-Headers'] = self._options['expose_headers']

        # Check if already setup the header Access-Control-Allow-Credentials
        if state['response']['headers'].get('Access-Control-Allow-Credentials'):
            self._options['credentials'] = json.loads(
                state['response']['headers']['Access-Control-Allow-Credentials']
            )

        if self._options['credentials']:
            state['response']['headers']['Access-Control-Allow-Credentials'] = 'true'

        # Check if already setup the header Access-Control-Allow-Origin
        if not state['response']['headers'].get('Access-Control-Allow-Origin'):
            state['response']['headers']['Access-Control-Allow-Origin'] = self.get_origin(
                state
            )

    after = add_cors_headers
    error = add_cors_headers
