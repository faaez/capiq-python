import requests,json
from requests.auth import HTTPBasicAuth
from settings import CAPIQ_USERNAME, CAPIQ_PASSWORD

class CapIQClient:
    _endpoint = 'https://sdk.gds.standardandpoors.com/gdssdk/rest/v2/clientservice.json'
    _headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept-Encoding': 'gzip,deflate'}

    def gdsp(self,tickers,mnemonics):
        req_array = []
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDSP","identifier":ticker,"mnemonic":mnemonic,"properties":{"PERIODTYPE":"IQ_FQ-2"}})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdst(self,tickers,mnemonics,start_date,end_date=None,frequency='D'):
        properties = {"STARTDATE":start_date,"FREQUENCY":frequency}
        if end_date:
            properties["ENDDATE"] = end_date

        req_array = []
        for ticker in tickers:
            for mnemonic in mnemonics:
                req_array.append({"function":"GDST","identifier":ticker,"mnemonic":mnemonic,"properties":properties})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()





