## PyMiddy

Heavily inspired from middyjs.

### Quick start

```python
from pymiddy import Middy
from pymiddy.middlewares import CORS

@Middy
def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'lorem ipsum dolor sit amet'
    }


handler.use(TestMiddleware(1)) \
    .use(CORS({
        'credentials': True,
        'origins': ['https://website.xyz/']
    }))
```

### Custom middlewares

A middleware class should have 3 methods:

```python
class MyCustomMiddleware(object):
    def before(self, state):
        pass

    def after(self, state):
        pass

    def error(self, state):
        pass
```

The `state` contains the following keys:
- `event` - the event which triggered the lambda function, passed from the aws handler
- `context` - the context from the aws handler
- `response` - the handler response, if any
- `exception` - during error handler you can have access to this key which contains the exception which triggered the error
