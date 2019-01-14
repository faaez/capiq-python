import datetime
import os

import requests
import json
import logging
import requests_cache
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class CiqServiceException(Exception):
    pass

class CapIQClient:
    _endpoint = 'https://api-ciq.marketintelligence.spglobal.com/gdsapi/rest/v3/clientservice.json'
    _headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'gzip,deflate'}
    _verify = True  # Disable SSL Checks for requests. Set to False to avoid SSL blocking in secured networks
    _username = None
    _password = None
    _debug = False
    _request_caching_enabled = False
    request_count = 0

    def __init__(self, username, password, verify=True, debug=False):
        assert username is not None
        assert password is not None
        assert verify is not None
        assert debug is not None
        self._username = username
        self._password = password
        self._verify = verify
        self._debug = debug
        if self._request_caching_enabled:
            self.request_count = self.get_cached_request_count()
        if not self._verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if self._debug:
            self.enable_request_debugging()
        else:
            self.enable_error_logging()
        # cache requests for 24 hours
        if self._request_caching_enabled:
            requests_cache.install_cache('capiq_cache', backend='sqlite', expire_after=86400, allowable_methods=('POST',))

    # This function retrieves a single data point for a point in time value for a mnemonic either current or
    # historical. Default inputs include a Mnemonic and a Security/Entity Identifier
    #
    # Returns a nested dictionary, where the primary key is the identifier and the secondary key is the mnemonic.
    # In case of an error, a None value is returned for that mnemonic and Cap IQ's error is logged
    def gdsp(self, identifiers, mnemonics, return_keys, properties=None):
        return self.make_request(identifiers, mnemonics, return_keys, properties, "GDSP", False)

    def gdspv(self, identifiers, mnemonics, return_keys, properties=None):
        return self.make_request(identifiers, mnemonics, return_keys, properties, "GDSPV", False)

    def gdst(self, identifiers, mnemonics, return_keys, start_date=None, end_date=None, frequency=None,
             properties=None):
        # properties or the start_date and frequency must be set
        if not properties:
            properties = []
            for i in range(0, len(mnemonics)):
                properties.append({})
        for p in properties:
            if frequency:
                p["FREQUENCY"] = frequency
            if start_date:
                p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date
        return self.make_request(identifiers, mnemonics, return_keys, properties, "GDST", True)

    def gdshe(self, identifiers, mnemonics, return_keys, start_date=None, end_date=None, properties=None):
        if not properties:
            properties = []
            for i in range(0, len(mnemonics)):
                properties.append({})
        for p in properties:
            if start_date:
                p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date

        return self.make_request(identifiers, mnemonics, return_keys, properties, "GDSHE", True)

    def gdshv(self, identifiers, mnemonics, return_keys, start_date=None, end_date=None, properties=None):
        if not properties:
            properties = []
            for i in range(0, len(mnemonics)):
                properties.append({})
        for p in properties:
            if start_date:
                p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date
        return self.make_request(identifiers, mnemonics, return_keys, properties, "GDSHV", False)

    def gdsg(self, identifiers, group_mnemonics, return_keys, properties=None):
        return self.make_request(identifiers, group_mnemonics, return_keys, properties, "GDSG", False)

    def get_request_count(self):
        return self.request_count

    def cache_request_count(self):
        # write the request_count to a file with todays date
        cache_file = open("./request_count_cache", "w")
        cache_file.write("{date},{request_count}".format(
            date=datetime.datetime.now().date(),
            request_count=self.request_count
        ))
        cache_file.close()

    def get_cached_request_count(self):
        # check for the cache file
        #   if present check if the date is today
        #       if the date is today then get the count and return it
        #       if the date is not today then overwrite the file with todays date and a count of zero and return 0
        # if the file is not present then create one with todays date and a count of 0
        if os.path.isfile("./request_count_cache"):
            cache_file = open("./request_count_cache", "r")
            cache_line = cache_file.readline()
            cache_data = cache_line.split(",")
            if cache_data[0] == str(datetime.datetime.now().date()):
                return int(cache_data[1])
            else:
                cache_file.close()
                self.request_count = 0
                self.cache_request_count()
                return self.request_count
        else:
            self.request_count = 0
            self.cache_request_count()
            return self.request_count

    def make_request(self, identifiers, mnemonics, return_keys, properties, api_function_identifier, multiple_results_expected):
        req_array = []
        returnee = {}
        mnemonic_return_keys = self.build_mnemonic_return_key_index(mnemonics, return_keys, properties)
        tmp_request_count = 0

        for identifier in identifiers:
            for i, mnemonic in enumerate(mnemonics):
                req_array.append({"function": api_function_identifier, "identifier": identifier, "mnemonic": mnemonic,
                                  "properties": properties[i] if properties else {}})
                tmp_request_count += 1
        req = {"inputRequests": req_array}
        response = requests.post(self._endpoint, headers=self._headers, data=json.dumps(req),
                                 auth=HTTPBasicAuth(self._username, self._password), verify=self._verify)
        if self._debug:
            logging.info("Cap IQ response")
            logging.info(response.json())
            logging.info("reponse from cache: {}".format(response.from_cache))
        if self._request_caching_enabled and not response.from_cache:
            self.request_count += tmp_request_count
            self.cache_request_count()

        if len(response.json()['GDSSDKResponse']) == 1 and \
                        len(response.json()['GDSSDKResponse'][0]) == 1 and \
                        "ErrMsg" in response.json()['GDSSDKResponse'][0].keys():
            # for catching service level issues such as request limit
            # this is an example of what we can catch:
            # {'GDSSDKResponse': [{'ErrMsg': 'Daily Request Limit of 10000 Exceeded'}]}
            raise CiqServiceException(response.json()['GDSSDKResponse'][0]["ErrMsg"])
        for return_index, ret in enumerate(response.json()['GDSSDKResponse']):
            identifier = ret['Identifier']
            if identifier not in returnee:
                returnee[identifier] = {}
            returned_properties = {}
            if "Properties" in ret:
                returned_properties = ret['Properties']
            if ret['ErrMsg']:
                logging.error(
                    'Cap IQ error for ' + identifier + ' + ' + ret['Mnemonic'] + ' query: ' + ret['ErrMsg'])
                returnee[identifier][
                    self.get_return_key(ret['Mnemonic'], returned_properties, mnemonic_return_keys)] = None
            else:
                for i_m, h_m in enumerate(ret["Headers"]):
                    if multiple_results_expected:
                        returnee[identifier][
                            self.get_return_key(ret['Mnemonic'], returned_properties, mnemonic_return_keys)] = []
                        for row in ret["Rows"]:
                            returnee[identifier][
                                self.get_return_key(ret['Mnemonic'], returned_properties, mnemonic_return_keys)
                            ].append(row['Row'])
                    else:
                        returnee[identifier][
                            self.get_return_key(ret['Mnemonic'], returned_properties, mnemonic_return_keys)
                        ] = ret['Rows'][i_m]['Row'][0]
        return returnee

    @staticmethod
    def build_mnemonic_return_key_index(mnemonics, return_keys, properties):
        mnemonic_return_keys = {}
        for index, mnemonic in enumerate(mnemonics):
            if mnemonic in mnemonic_return_keys:
                mnemonic_return_keys[mnemonic].append({"key": return_keys[index], "properties": properties[index]})

            else:
                mnemonic_return_keys[mnemonic] = [{"key": return_keys[index], "properties": properties[index]}]
        return mnemonic_return_keys

    @staticmethod
    def get_return_key(mnemonic, properties, mnemonics_to_return_key_index):
        logging.info("mnemonics_to_return_key_index")
        logging.info(mnemonics_to_return_key_index)
        if len(mnemonics_to_return_key_index[mnemonic]) == 1:
            return mnemonics_to_return_key_index[mnemonic][0]["key"]
        else:
            for index, return_key in enumerate(mnemonics_to_return_key_index[mnemonic]):
                match = True
                logging.info(properties)
                for property_name, property_value in properties.items():
                    if not (property_name.upper() in return_key["properties"] and \
                                        return_key["properties"][property_name.upper()] == property_value.replace(" ", "+")):
                        match = False
                if match:
                    return return_key["key"]

    @staticmethod
    def enable_request_debugging():
        # Enabling debugging at http.client level (requests->urllib3->http.client)
        # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
        # the only thing missing will be the response.body which is not logged.
        try:  # for Python 3
            from http.client import HTTPConnection
        except ImportError:
            from requests.packages.urllib3.connectionpool import HTTPConnection
        HTTPConnection.debuglevel = 1

        logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    @staticmethod
    def enable_error_logging():
        logging.basicConfig()  # you need to initialize logging, otherwise you will not see anything from requests
        logging.getLogger().setLevel(logging.ERROR)
