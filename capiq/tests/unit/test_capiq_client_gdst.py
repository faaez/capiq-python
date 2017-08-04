import unittest

from mock import mock

from capiq.capiq_client import CapIQClient


def mocked_gdst_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data
    """
    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
    """
    if args[0] is not None:
        return MockResponse({"GDSSDKResponse": [      {
            "Headers": ["IQ_CLOSEPRICE"],
            "Rows": [{"Row": ["46.80"]}],
            "NumCols": 1,
            "Seniority": "",
            "Mnemonic": "IQ_CLOSEPRICE",
            "Function": "GDST",
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

def mocked_gdst_no_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    """
    if args[0] == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
    """
    if args[0] is not None:
        return MockResponse(
            {
                "GDSSDKResponse":
                    [
                        {
                            "Headers": ["IQ_CLOSEPRICE"],
                            "Rows": [{"Row": ["46.80"]}],
                            "NumCols": 1,
                            "Seniority": "",
                            "Mnemonic": "IQ_CLOSEPRICE",
                            "Function": "GDST",
                            "ErrMsg": "SOME ERROR",
                            "Properties": {},
                            "StartDate": "",
                            "NumRows": 1,
                            "CacheExpiryTime": "0",
                            "SnapType": "",
                            "Frequency": "",
                            "Identifier": "TRIP:",
                            "Limit": ""
                        }
                    ]
            }, 200)

class TestCapiqClientGdst(unittest.TestCase):

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdst_data_requests_post)
    def test_gdst_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdst(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], properties=[{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': [['46.80']]}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdst_data_requests_post)
    def test_gdst_data_no_properties(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdst(
            ["TRIP"],
            ["IQ_CLOSEPRICE"],
            ["close_price"],
            start_date="12/19/1980",
            end_date="12/19/2000",
            frequency="M"
        )
        self.assertEqual(return_value, {'TRIP:': {'close_price': [['46.80']]}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdst_no_data_requests_post)
    def test_gdst_no_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdst(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': None}})