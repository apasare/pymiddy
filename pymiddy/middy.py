class Middy(object):
    def __init__(self, handler):
        self.handler = handler
        self.before_middlewares = []
        self.after_middlewares = []
        self.error_middlewares = []

    def run_middlewares(self, middlewares, state):
        for middleware in middlewares:
            response = middleware(state)
            if response is not None:
                return response

    def __call__(self, event, context):
        state = {
            'event': event,
            'context': context,
            'response': {},
            'exception': None
        }

        try:
            response = self.run_middlewares(self.before_middlewares, state)
            if response:
                return response

            state['response'] = self.handler(event, context)

            response = self.run_middlewares(self.after_middlewares, state)
            if response:
                return response
        except BaseException as e:
            state['exception'] = e
            self.run_middlewares(self.error_middlewares, state)

        return state['response']

    def use(self, middleware):
        if callable(getattr(middleware, 'before', None)):
            self.before_middlewares.append(getattr(middleware, 'before'))
        if callable(getattr(middleware, 'after', None)):
            self.after_middlewares.insert(0, getattr(middleware, 'after'))
        if callable(getattr(middleware, 'error', None)):
            self.error_middlewares.append(getattr(middleware, 'error'))

        return self


# experimental
def middyfy(middlewares):
    def handler_wrapper(handler):
        if isinstance(handler, Middy):
            return handler

        handler_proxy = Middy(handler)

        if isinstance(middlewares, list):
            list(map(handler_proxy.use, middlewares))
        elif isinstance(middlewares, object):
            handler_proxy.use(middlewares)

        return handler_proxy

    return handler_wrapper
