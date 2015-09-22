# capiq-python
Thin Python wrapper for CapIQ's REST API

##Status

The wrapper is functional, but extremely thin. Would benefit from more functionality and documentation. 

###TODO

- [ ] Implement caching functionality
- [ ] Write tests

##Getting Started

Create a settings.py file and specify your CapIQ username and password as follows:

    CAPIQ_USERNAME = {{username}}
    CAPIQ_PASSWORD = {{password}}

All functions in this client take 'identifiers' as an argument. Capital IQ uses identifiers to identify companies, which could be CUSIP, CINS, ISIN, SEDOL, DUNS ID, GVKEY, Ticker or S&P Capital IQ ID. When using tickers, conform to the TICKER:EXCHANGE convention, as in, "IBM:NYSE" but beware that for some mnemonics, Capital IQ returns tickers in the EXCHANGE:TICKER convention, as in, "NYSE:IBM." Nobody (including Capital IQ themselves, most likely) knows why. 

