from influxdb import InfluxDBClient
import pandas as pd
from datetime import datetime
from time import  sleep


class influxT0Pandas():

    def __init__(self, market, data_type):
        self.localhost = 'localhost'
        self.port = 8086

        self.client = InfluxDBClient(host=self.localhost, port=self.port)

        if market == 'binance':
            self.market = 'Binance'
            self.db_tab_market_name = 'BINANCE'

        elif market == 'coinbase':
            self.market = 'CoinBase'
            self.db_tab_market_name = 'COINBASE'


        else:
            raise ValueError('Market not implemented')

        if data_type == 'trades': self.data_type = 'trades'
        else: raise ValueError('Data type not recognised ')


    def db_list(self):
        print(self.client.get_list_database())

    def connect_to_market(self):
        self.client.switch_database(self.market)

    def get_dataframe(self):
        query = f'SELECT * FROM "{self.data_type}-{self.db_tab_market_name}"'
        self.df =pd.DataFrame(self.client.query(query).get_points())

    def format_data(self):
        self.df['receive_timestamp'] =  self.df.timestamp.apply(lambda x:
                                                                datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f'))
        self.df['write_timestamp'] =  self.df.time
        self.df = self.df.drop(columns = ['id','time','timestamp'])

    @property
    def get_data(self):
        self.connect_to_market()
        self.get_dataframe()
        self.format_data()
        return self.df

    def get_count(self):
        print(len(self.df))






if __name__ == '__main__':
    md = influxT0Pandas(market='binance', data_type='trades')
    md.connect_to_market()
    md.get_data
    md.get_count()
