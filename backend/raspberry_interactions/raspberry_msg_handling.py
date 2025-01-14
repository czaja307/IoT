from controllers.tag import create_tag, update_tag, get_tag
from schemas.tag import TagCreate, TagUpdate
from database import get_db
from models.product import Product as mProduct
from schemas.product import Product as sProduct
from mqtt_conf import STATUS_NOK, STATUS_OK

class RaspberryMsgHandling:
    @staticmethod
    def on_terminal_msg(msg):
        tag = int(msg)
        terminal_id = int(topic.split("/")[2])
        prod = int(ServerCommunications().terminals_products_dict[terminal_id])
        if not prod:
            return STATUS_NOK

        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        if tag_from_db:
            update_tag(db, tag, TagUpdate(id=tag, product_id=prod))
        else:
            create_tag(db, TagCreate(id=tag, product_id=prod))
        return STATUS_OK


    @staticmethod
    def on_checkout_msg(msg):
        tag = int(msg)
        get_db_v = get_db()
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        s_prod = sProduct.model_validate(tag_from_db.product)
        print(s_prod.model_dump())
        return str(s_prod.model_dump())
