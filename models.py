import re
import uuid
import datetime

from schematics.models import Model
from schematics.types import StringType, DateTimeType
from schematics.exceptions import ModelValidationError
from schematics.types import BaseType

import phonenumbers
from phonenumbers import NumberParseException

# Use phonenumbers library


class InvalidUKMobileNumberException(Exception):
    pass


class UKMobileNumberType(BaseType):
    MESSAGES = {
        'number': 'Value must be a valid UK mobile number.',
    }

    def to_primitive(self, value):
        return value

    def validate_number(self, value):
        if not isinstance(value, basestring):
            raise InvalidUKMobileNumberException('Number must be unicode or str to parse.')  
        
        try:
            number = phonenumbers.parse(value, None)    
        except NumberParseException:
            raise InvalidUKMobileNumberException(self.messages['number'])


class Recipient(Model):
    number = UKMobileNumberType(required=True)
    created_at = DateTimeType(default=datetime.datetime.now)


class RecipientStore(object):

    def __init__(self):
        self._store = {}

    def add(self, recipient):
        key = str(uuid.uuid4())
        self._store[key] = recipient
        return key
