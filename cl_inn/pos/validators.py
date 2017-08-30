from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import RegexValidator

class GeneralCMSValidator(object):
    """Contains general validators that can be applied in multiple situations."""
    name_validator = RegexValidator(r'^[\u0621-\u064Aa-zA-Z][\u0621-\u064Aa-zA-Z0-9]*([ ]?[\u0621-\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.') 



