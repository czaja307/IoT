from controllers.tag import create_tag, update_tag, get_tag
from schemas.tag import TagCreate, TagUpdate
from database import get_db
from models.product import Product
import json

class RaspberryMsgHandling():
    def on_terminal_msg(self, msg):
        tag = int(msg)
        prod = 2
        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        if tag_from_db:
            update_tag(db, tag, TagUpdate(id=tag, product_id=prod))
        else:
            create_tag(db, TagCreate(id=tag, product_id=prod))


    def on_checkout_msg(self, msg):
        tag = int(msg)
        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        product: Product = tag_from_db.product
        print(product.to_json())
        return product.to_json()
