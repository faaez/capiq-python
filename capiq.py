import requests,json,logging
from requests.auth import HTTPBasicAuth
from settings import CAPIQ_USERNAME, CAPIQ_PASSWORD

class CapIQClient:
    _endpoint = 'https://sdk.gds.standardandpoors.com/gdssdk/rest/v2/clientservice.json'
    _headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept-Encoding': 'gzip,deflate'}

    # This function retrieves a single data point for a point in time value for a mnemonic either current or
    # historical. Default inputs include a Mnemonic and a Security/Entity Identifier
    #
    # Returns a nested dictionary, where the primary key is the identifier and the secondary key is the mnemonic. In case of an error,
    # a None value is returned for that mnemonic and Cap IQ's error is logged
    def gdsp(self,identifiers,mnemonics,properties=None):
        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(mnemonics):
                req_array.append({"function":"GDSP","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i] if properties else {}})
        req = {"inputRequests":req_array}
        response = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        returnee = {}
        for r in response.json()['GDSSDKResponse']:
            identifier = r['Identifier']
            if identifier not in returnee:
                returnee[identifier] = {}
            for i,h in enumerate(r['Headers']):
                if ret['ErrMsg']:
                    logging.error('Cap IQ error for '+identifier+' + '+h+' query: '+r['ErrMsg'])
                    returnee[identifier][h] = None
                else:
                    returnee[identifier][h] = r['Rows'][i]['Row'][0]
        return returnee

    def gdspv(self,identifiers,mnemonics,properties=None):
        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(mnemonics):
                req_array.append({"function":"GDSPV","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i] if properties else {}})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdst(self,identifiers,mnemonics,start_date,end_date=None,frequency='D',properties=None):
        if not properties:
            properties = []
            for i in range(0,len(mnemonics)):
                properties.append({})
        for p in properties:
            p["FREQUENCY"] = frequency
            p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date

        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(mnemonics):
                req_array.append({"function":"GDST","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i]})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdshe(self,identifiers,mnemonics,start_date=None,end_date=None,properties=None):
        if not properties:
            properties = []
            for i in range(0,len(mnemonics)):
                properties.append({})
        for p in properties:
            if start_date:
                p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date

        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(mnemonics):
                req_array.append({"function":"GDSHE","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i]})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdshv(self,identifiers,mnemonics,start_date=None,end_date=None,properties=None):
        if not properties:
            properties = []
            for i in range(0,len(mnemonics)):
                properties.append({})
        for p in properties:
            if start_date:
                p["STARTDATE"] = start_date
            if end_date:
                p["ENDDATE"] = end_date

        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(mnemonics):
                req_array.append({"function":"GDSHV","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i]})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()

    def gdsg(self,identifiers,group_mnemonics,properties=None):
        req_array = []
        for identifier in identifiers:
            for i,mnemonic in enumerate(group_mnemonics):
                req_array.append({"function":"GDSG","identifier":identifier,"mnemonic":mnemonic,"properties":properties[i] if properties else {}})
        req = {"inputRequests":req_array}
        r = requests.post(self._endpoint,headers=self._headers,data='inputRequests='+json.dumps(req),auth=HTTPBasicAuth(CAPIQ_USERNAME,CAPIQ_PASSWORD))
        return r.json()






