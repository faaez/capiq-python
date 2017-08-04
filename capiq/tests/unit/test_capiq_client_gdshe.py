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

def mocked_gdsg_multi_data_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] is not None:
        return MockResponse(
            {'GDSSDKResponse': [{'Headers': ['IQ_VWAP', 'AsOfDate'],
                                 'Rows': [{'Row': ['239.900000', '5/23/2017']},
                                          {'Row': ['240.410000', '5/24/2017']},
                                          {'Row': ['241.710000', '5/25/2017']},
                                          {'Row': ['241.590000', '5/26/2017']}],
                                 'Seniority': '', 'NumCols': 2, 'Mnemonic': 'IQ_VWAP', 'NumRows': 4,
                                 'CacheExpiryTime': '0',
                                 'ErrMsg': '', 'Function': 'GDSHE', 'Frequency': '', 'Identifier': 'TRIP:',
                                 'Limit': '',
                                 'Properties': {'startdate': '05/23/2017', 'enddate': '05/29/2017'}},
                                {'Headers': ['IQ_VWAP', 'AsOfDate'],
                                 'Rows': [{'Row': ['240.040000', '5/16/2017']},
                                          {'Row': ['237.870000', '5/17/2017']},
                                          {'Row': ['236.640000', '5/18/2017']},
                                          {'Row': ['238.330000', '5/19/2017']},
                                          {'Row': ['239.210000', '5/22/2017']}], 'Seniority': '', 'NumCols': 2,
                                 'Mnemonic': 'IQ_VWAP', 'NumRows': 5, 'CacheExpiryTime': '0', 'ErrMsg': '',
                                 'Function': 'GDSHE', 'Frequency': '', 'Identifier': 'TRIP:', 'Limit': '',
                                 'Properties': {'startdate': '05/16/2017', 'enddate': '05/22/2017'}}]}
            , 200)

class TestCapiqClientGdshe(unittest.TestCase):

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_data_requests_post)
    def test_gdshe_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], properties=[{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': [['46.80']]}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_no_data_requests_post)
    def test_gdshe_no_data(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
        self.assertEqual(return_value, {'TRIP:': {'close_price': None}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdshe_data_requests_post)
    def test_gdshe_data_no_properties(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(
            ["TRIP"],
            ["IQ_CLOSEPRICE"],
            ["close_price"],
            start_date="12/19/1980",
            end_date="12/19/2000"
        )
        self.assertEqual(return_value, {'TRIP:': {'close_price': [['46.80']]}})

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdsg_multi_data_requests_post)
    def test_gdshe_multi_data_with_name_collision(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        return_value = ciq_client.gdshe(["TRIP", "TRIP"], ["IQ_VWAP", "IQ_VWAP"], ["vwap1", "vwap2"], properties=[
            {"STARTDATE": "05/23/2017", "ENDDATE": "05/29/2017"},
            {"STARTDATE": "05/16/2017", "ENDDATE": "05/22/2017"}
        ])
        self.assertEqual(
            return_value, {
                'TRIP:': {
                    'vwap1': [
                        ['239.900000', '5/23/2017'],
                        ['240.410000', '5/24/2017'],
                        ['241.710000', '5/25/2017'],
                        ['241.590000', '5/26/2017']
                    ],
                    'vwap2': [
                        ['240.040000', '5/16/2017'],
                        ['237.870000', '5/17/2017'],
                        ['236.640000', '5/18/2017'],
                        ['238.330000', '5/19/2017'],
                        ['239.210000', '5/22/2017']
                    ]
                }
            }
        )