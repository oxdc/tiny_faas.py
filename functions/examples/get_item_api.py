path = '/items/{item_id}'
method = 'get'
is_async = False


def execute(item_id: int, q: str = None):
    return {'item_id': item_id, 'q': q}
