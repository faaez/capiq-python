import unittest

from mock import mock

from capiq.capiq_client import CapIQClient


def mocked_gdspv_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] is not None:
        return MockResponse({"GDSSDKResponse": [      {
            "Headers": ["IQ_CLOSEPRICE"],
            "Rows": [{"Row": ["46.80"]}],
            "NumCols": 1,
            "Seniority": "",
            "Mnemonic": "IQ_CLOSEPRICE",
            "Function": "GDSPV",
            "ErrMsg": None,
            "Properties": {},
            "StartDate": "",
            "NumRows": 1,
            "CacheExpiryTime": "0",
            "SnapType": "",
            "Frequency": "",
            "Identifier": "TRIP:",
            "Limit": ""
        }]}, 200)

def mocked_gdspv_no_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] is not None:
        return MockResponse({"GDSSDKResponse": [      {
      "Headers": ["IQ_CLOSEPRICE"],
      "Rows": [{"Row": ["46.80"]}],
      "NumCols": 1,
      "Seniority": "",
      "Mnemonic": "IQ_CLOSEPRICE",
      "Function": "GDSPV",
      "ErrMsg": "SOME ERROR",
      "Properties": {},
      "StartDate": "",
      "NumRows": 1,
      "CacheExpiryTime": "0",
      "SnapType": "",
      "Frequency": "",
      "Identifier": "TRIP:",
      "Limit": ""
   }]}, 200)

class TestCapiqClientGdspv(unittest.TestCase):

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdspv_data_requests_post)
    def test_gdspv_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdspv(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': '46.80'}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdspv_no_data_requests_post)
    def test_gdspv_no_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdspv(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': None}})