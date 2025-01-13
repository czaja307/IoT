from controllers.tag import create_tag, update_tag, get_tag
from raspberry_interactions import ServerCommunications
from schemas.tag import TagCreate, TagUpdate
from database import get_db
from schemas.product import Product as sProduct


class RaspberryMsgHandling:
    @staticmethod
    def on_terminal_msg(msg):
        tag = int(msg)
        prod = 2
        terminal = 1
        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        if tag_from_db:
            update_tag(db, tag, TagUpdate(id=tag, product_id=prod))
        else:
            create_tag(db, TagCreate(id=tag, product_id=prod))
        ServerCommunications().terminals_products_dict[terminal] = prod

    @staticmethod
    def on_checkout_msg(msg):
        tag = int(msg)
        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        s_prod = sProduct.model_validate(tag_from_db.product)
        print(s_prod.model_dump())
        return str(s_prod.model_dump())
