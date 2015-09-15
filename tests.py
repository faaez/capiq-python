from capiq import CapIQClient

if __name__ == '__main__':
    client = CapIQClient()
    print client.gdshe(['WMT:'],['IQ_CLOSEPRICE'],start_date='11/12/2010',end_date='11/18/2010')
    # print client.gdsg(['WMT:'],['BASIC_SECURITY_DESCRIPTION'])