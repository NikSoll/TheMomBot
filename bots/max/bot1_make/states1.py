from enum import Enum

class BookingStates(str, Enum):
    CHOOSING_MASTER = "choosing_master"
    CHOOSING_DATE = "choosing_date"
    CHOOSING_TIME = "choosing_time"
    ENTERING_NAME = "entering_name"
    ENTERING_PHONE = "entering_phone"
    ENTERING_COMMENT = "entering_comment"