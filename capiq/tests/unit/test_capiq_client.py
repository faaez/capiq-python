import unittest

from mock import mock

from capiq.capiq_client import CapIQClient, CiqServiceException

orig_import = __import__

def mocked_gdsp_error_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] is not None:
        return MockResponse({'GDSSDKResponse': [{'ErrMsg': 'Daily Request Limit of 10000 Exceeded'}]}, 200)

class TestCapiqClient(unittest.TestCase):

    def test_verify_true(self):
        ciq_client = CapIQClient("username", "password", verify=True)
        self.assertEqual(ciq_client._verify, True)

    def test_verify_false(self):
        ciq_client = CapIQClient("username", "password", verify=False)
        self.assertEqual(ciq_client._verify, False)

    def test_debug_true(self):
        ciq_client = CapIQClient("username", "password", debug=True)
        self.assertEqual(ciq_client._debug, True)

    def test_debug_false(self):
        ciq_client = CapIQClient("username", "password", )
        self.assertEqual(ciq_client._debug, False)

    def test_python_2_exception(self):
        def import_mock(name, *args):

            if name == 'http.client':
                raise ImportError
            return orig_import(name, *args)

        with mock.patch('builtins.__import__', side_effect=import_mock):
            capiq_client = CapIQClient("username", "password", verify=False)
            self.assertIsInstance(capiq_client, CapIQClient)

    @mock.patch('capiq.capiq_client.requests.post', side_effect=mocked_gdsp_error_response)
    def test_gdsp_api_service_error(self, mocked_post):
        ciq_client = CapIQClient("username", "password")
        with self.assertRaises(CiqServiceException):
            ciq_client.gdsp(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], [{}])
