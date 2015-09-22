from capiq import CapIQClient

metrics = {'comps':['IQ_QUICK_COMP',{}],'percent_of_shares_outstanding':['IQ_SHORT_INTEREST_PERCENT',{}], 'rolling_vol_30':['IQ_VOLATILITY',{}], 'price':['IQ_CLOSEPRICE',{}],
        'norm_pe_ratio':['IQ_PE_NORMALIZED',{}],'ebitda_margin_annual':['IQ_EBITDA_MARGIN',{'PERIODTYPE':'IQ_FY'}],'ebitda_margin_ttm':['IQ_EBITDA_MARGIN',{'PERIODTYPE':'IQ_LTM'}], 
        'shares_outstanding':['IQ_SHARESOUTSTANDING',{}], 'capex_to_revenue_ttm':['IQ_CAPEX_PCT_REV',{}],'price_to_book_value':['IQ_PBV',{}],
        'revenues_ttm':['IQ_TOTAL_REV',{'PERIODTYPE':'IQ_LTM'}],'revenues':['IQ_TOTAL_REV',{'PERIODTYPE':'IQ_FQ'}],'cash_and_equivalents':['IQ_CASH_EQUIV',{}],'one_month_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-1M','MULTIPLYING_FACTOR':0.01}],
        'three_month_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-3M','MULTIPLYING_FACTOR':0.01}],'six_month_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-6M','MULTIPLYING_FACTOR':0.01}],'one_year_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-1Y','MULTIPLYING_FACTOR':0.01}],
        'three_year_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-3Y','MULTIPLYING_FACTOR':0.01}], 'five_year_total_return':['IQ_CLOSEPRICE_ADJ',{'PERIODTYPE':'-5Y','MULTIPLYING_FACTOR':0.01}], 
        'return_on_invested_capital':['IQ_RETURN_CAPITAL',{}], 'revenues_annual':['IQ_TOTAL_REV',{'PERIODTYPE':'IQ_FY'}],'ebit_margin_annual':['IQ_EBIT_MARGIN',{'PERIODTYPE':'IQ_FY'}],
        'volume':['IQ_VOLUME',{}]}


if __name__ == '__main__':
    client = CapIQClient()
    # print client.gdshe(['WMT:'],['IQ_CLOSEPRICE'],start_date='11/12/2010',end_date='11/18/2010')
    # mnemonics = []
    # properties = []
    # for m in metrics:
    #     mnemonics += [metrics[m][0]]
    #     properties += [metrics[m][1]]
    # r = client.gdsp(['IBM:'],mnemonics,properties=properties)
    # for k in r:
    #     for i in r[k]:
    #         if 'Headers' not in i:
    #             print 'Error:', i
    #             continue
    #         for ii in range(0,len(i['Headers'])):
    #             print i['Headers'][ii],':',i['Rows'][ii]


    # print client.gdsg(['WMT:'],['BASIC_SECURITY_DESCRIPTION'])

    # print client.gdshe(['nyse:ibm'],['IQ_QUICK_COMP'],properties=[{'StartRank':1,'EndRank':5}])
    # print client.gdshv(['^ftse'],['IQ_CONSTITUENTS'],properties=[{'StartRank':1,'EndRank':5}])
    metrics_map = {'name':'IQ_COMPANY_NAME','industry':'IQ_INDUSTRY','sector':'IQ_INDUSTRY_SECTOR','profile':'IQ_BUSINESS_DESCRIPTION','company_url':'IQ_COMPANY_WEBSITE'}
    query = []
    for m in metrics_map:
        query.append(metrics_map[m])

    print client.gdsp(['ibm:','aapl:'],query)

    # print client.gdsp(['ibm:'],['IQ_COMPANY_NAME'])
    # print client.gdsg(['ibm:nyse'],['BASIC_SECURITY_DESCRIPTION'])

    # print client.gdst(['IBM:'],['TRACE_TRADE_30D_PRICE_VOLATILITY'],start_date="08/18/2015",properties={'frequency':"Daily",'currencyId':"USD",'currencyConversionModeId':"HISTORICAL"})