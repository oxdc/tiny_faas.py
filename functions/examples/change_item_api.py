from pydantic import BaseModel


path = '/items/{item_id}'
method = 'put'
is_async = False


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


def execute(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}
