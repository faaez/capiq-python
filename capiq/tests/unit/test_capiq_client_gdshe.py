import unittest

from mock import mock

from capiq.capiq_client import CapIQClient


def mocked_gdshe_data_requests_post(*args, **kwargs):
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
            "Function": "GDSHE",
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

def mocked_gdshe_no_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

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
                            "Function": "GDSHE",
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

class TestCapiqClientGdshe(unittest.TestCase):

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_data_requests_post)
    def test_gdshe_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], properties=[{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': '46.80'}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_no_data_requests_post)
    def test_gdshe_no_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': None}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_data_requests_post)
    def test_gdst_data_no_properties(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(
            ["TRIP"],
            ["IQ_CLOSEPRICE"],
            ["close_price"],
            start_date="12/19/1980",
            end_date="12/19/2000"
        )
        self.assertEqual(return_value, {'TRIP:': {'close_price': '46.80'}})