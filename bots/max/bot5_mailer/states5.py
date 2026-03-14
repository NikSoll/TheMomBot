from enum import Enum

class MailerStates(str, Enum):
    CHOOSING_GROUP = "choosing_group"
    ENTERING_TEXT = "entering_text"
    ENTERING_PHOTO = "entering_photo"
    CONFIRM = "confirm"