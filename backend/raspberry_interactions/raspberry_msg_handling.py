from controllers.tag import create_tag, update_tag, get_tag, delete_tag
from controllers.purchase import create_purchase
from raspberry_interactions import ServerCommunications
from schemas.tag import TagCreate, TagUpdate
from database import get_db
from models.product import Product as mProduct
from schemas.product import Product as sProduct
from schemas.purchase import PurchaseCreate, ProductQuantityCreate
from mqtt_conf import STATUS_NOK, STATUS_OK
from collections import defaultdict

class RaspberryMsgHandling:

    @staticmethod
    def _create_purchase(product_dict):
        products_for_purchase = [
            ProductQuantityCreate(product_id=value["product"].id, quantity=value["quantity"])
            for value in product_dict.values()
        ]

        purchase = PurchaseCreate(products=products_for_purchase)
        return purchase

    @staticmethod
    def _return_product_data(msg, get_db_v):
        tag = int(msg)
        db = next(get_db_v)
        tag_from_db = get_tag(db, tag)
        s_prod = sProduct.model_validate(tag_from_db.product)
        print(s_prod.model_dump())
        return str(s_prod.model_dump())

    def _process_purchase(parts, get_db_v):
        db = next(get_db_v)
        prod_quants = defaultdict(lambda: {"product": None, "quantity": 0})
        for tag in parts[1:]:
            tag_from_db = get_tag(db, tag)
            s_prod = sProduct.model_validate(tag_from_db.product)
            prod_id = tag_from_db.product_id
            if prod_id not in prod_quants:
                prod_quants[prod_id]["product"] = s_prod
            prod_quants[prod_id]["quantity"] += 1
            delete_tag(db, get_db_v)
        purchase = RaspberryMsgHandling._create_purchase(prod_quants)
        create_purchase(db, purchase)
        return None

    @staticmethod
    def on_terminal_msg(msg, topic):
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
        parts = msg.split("#")
        get_db_v = get_db()
        if len(parts) == 1:
            return RaspberryMsgHandling._return_product_data(msg, get_db_v)
        elif len(parts) > 1 and parts[0] == "BUY":
            return RaspberryMsgHandling._process_purchase(parts, get_db_v)
        else:
            print("Illegal message format")
            return None

