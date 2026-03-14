from enum import Enum

class ShopStates(str, Enum):
    BROWSING = "browsing"
    VIEWING_PRODUCT = "viewing_product"
    IN_CART = "in_cart"
    ENTERING_NAME = "entering_name"
    ENTERING_PHONE = "entering_phone"
    ENTERING_ADDRESS = "entering_address"
    ENTERING_COMMENT = "entering_comment"