import pytest
import json
from falcon import HTTP_404, HTTP_405, HTTP_200, HTTP_400

from models import Recipient, InvalidUKMobileNumberException

from api import api
from falcon.testing import TestBase, create_environ


""" Model Tests """


@pytest.fixture
def test_recipient():
    return Recipient(dict(number='+447427600266'))


def test_valid_uk_number_ok(test_recipient):
    assert test_recipient.validate() is None


def test_invalid_uk_number(test_recipient):
    with pytest.raises(InvalidUKMobileNumberException):
        bad_recipient = Recipient(dict(number='123456'))
        bad_recipient.validate()


def test_not_correct_type(test_recipient):
    with pytest.raises(InvalidUKMobileNumberException):
        bad_recipient = Recipient(dict(number=44123456))
        bad_recipient.validate()


""" Functional Tests """


class TestAPI(TestBase):

    def before(self):
        self.api = api

    def test_404_on_root(self):
        self.simulate_request('/')
        self.assertEqual(self.srmock.status, HTTP_404)

    def test_405_on_root(self):
        self.simulate_request('/recipient/')
        self.assertEqual(self.srmock.status, HTTP_405)

    def test_can_create_recipient(self):
        context = dict(method='POST', 
                       body=json.dumps(dict(number='+447427600266')),
                       headers=dict(Content_Type='application/json')
        )
        self.simulate_request('/recipient', **context)
        self.assertEqual(self.srmock.status, HTTP_200)

    def test_barf_on_invalid_recipient_number(self):
        context = dict(method='POST', 
                       body=json.dumps(dict(number='123456')),
                       headers=dict(Content_Type='application/json')
        )
        self.simulate_request('/recipient/', **context)
        self.assertEqual(self.srmock.status, HTTP_400)
