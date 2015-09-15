import requests,json
from requests.auth import HTTPBasicAuth
from settings import CAPIQ_USERNAME, CAPIQ_PASSWORD

class CapIQClient:
    _endpoint = 'https://sdk.gds.standardandpoors.com/gdssdk/rest/v2/clientservice.json'
    _headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept-Encoding': 'gzip,deflate'}

    def gdsp(self,tickers,mnemonics,properties=None):
        req_array = []
        if not properties:
            properties = {}
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDSP","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdspv(self,tickers,mnemonics,properties=None):
        req_array = []
        if not properties:
            properties = {}
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDSPV","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdst(self,tickers,mnemonics,start_date,end_date=None,frequency='D',properties=None):
        if not properties:
            properties = {}
        properties["FREQUENCY"] = frequency
        properties["STARTDATE"] = start_date
        if end_date:
            properties["ENDDATE"] = end_date

        req_array = []
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDST","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdshe(self,tickers,mnemonics,start_date,end_date=None,properties=None):
        if not properties:
            properties = {}
        properties["STARTDATE"] = start_date
        if end_date:
            properties["ENDDATE"] = end_date

        req_array = []
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDSHE","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdshv(self,tickers,mnemonics,start_date,end_date=None,properties=None):
        if not properties:
            properties = {}
        properties["STARTDATE"] = start_date
        if end_date:
            properties["ENDDATE"] = end_date

        req_array = []
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDSHV","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdsg(self,tickers,group_mnemonics,properties=None):
        if not properties:
            properties = {}
        req_array = []
        for ticker in tickers:
            for mnemonic in group_mnemonics:
                req_array.append({"function":"GDSG","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()






