from capiq import CapIQClient

if __name__ == '__main__':
    client = CapIQClient()
    print client.gdst(['WMT:'],['IQ_TOTAL_REV'],start_date='11/12/2010',end_date='12/12/2011',frequency='Q')