# capiq-python
Thin Python wrapper for CapIQ's REST API

##Status

The wrapper is functional, but extremely thin. Would benefit from more functionality and documentation. 

###TODO

All function should be tested to confirm they work as expected.

##Getting Started

Install the package using pip. 
```bash
pip install git+git://github.com/guydmann/capiq-python.git --upgrade
```

To initialize the wrapper import the client and initialize it with the username and password.  If you want to stop SSL verification also pass verify=False.  By default SSL certificates will be verified.
```python
from capiq.capiq_client import CapIQClient
ciq_client = CapIQClient(USERNAME, PASSWORD)
```

To make calls to the capiq api 6 different functions which are documented in the Cap IQ documentation.  Each function takes a list of identifiers, mnemonics, return keys and properties.
```python
ciq_client = CapIQClient("username", "password")
return_value = ciq_client.gdsg(["TRIP"], ["IQ_CLOSEPRICE"], ["close_price"], properties=[{}])
```

Capital IQ uses identifiers to identify companies, which could be CUSIP, CINS, ISIN, SEDOL, DUNS ID, GVKEY, Ticker or S&P Capital IQ ID. When using tickers, conform to the TICKER:EXCHANGE convention, as in, "IBM:NYSE" but beware that for some mnemonics, Capital IQ returns tickers in the EXCHANGE:TICKER convention, as in, "NYSE:IBM." Nobody (including Capital IQ themselves, most likely) knows why.

Mnemonics are strings which key a specific piece of data from Cap IQ. For the specifics see the Cap IQ API Developer Guide.

Return keys map the cap iq mnemonics to new variable names in the return object, this is useful if you are pulling the same data for multiple time frames and you would like them to be easily distinguishable.

Properties identify the time frame to filter the requested data on.  For the specifics see the Cap IQ API Developer Guide. 

