import asyncio
from cryptofeed.backends.influxdb import TradeInflux, FundingInflux, BookInflux, BookDeltaInflux, TickerInflux
from cryptofeed.backends.arctic import TradeArctic
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Coinbase, Binance
from cryptofeed.defines import L2_BOOK, BID, ASK, TRADES, TICKER, COINBASE
from cryptofeed.defines import (L2_BOOK, L3_BOOK, TRADES, TICKER, VOLUME, FUNDING, UNSUPPORTED, BITFINEX, GEMINI, BITMAX,
                                POLONIEX, HITBTC, BITSTAMP, COINBASE, BITMEX, KRAKEN, KRAKEN_FUTURES, BINANCE, EXX, HUOBI, HUOBI_US, HUOBI_DM, OKCOIN,
                                OKEX, COINBENE, BYBIT, FTX, TRADES_SWAP, TICKER_SWAP, L2_BOOK_SWAP, TRADES_FUTURES, TICKER_FUTURES, L2_BOOK_FUTURES,
                                LIMIT, MARKET, FILL_OR_KILL, IMMEDIATE_OR_CANCEL, MAKER_OR_CANCEL, DERIBIT, INSTRUMENT, BITTREX, BITCOINCOM, BINANCE_US)

from cryptofeed.pairs import gen_pairs



class getMarketData():


    def __init__(self):
        self.localhost = 'http://localhost:8086'
        pass


    def set_market(self, market):

        if market == 'binance':
            self.market = Binance
            self.market_function  = BINANCE
            self.db_name = 'Binance'


        elif market == 'coinbase':
            self.market = Coinbase
            self.market_function = COINBASE
            self.db_name = 'CoinBase'

        else:
            raise ValueError("market not implemented")

    def set_sym(self, sym):
        self.sym = sym
        #get list of traded syms in the market

        self.get_sym_list()
        #check if sym in sym list

        if not self.sym  in self.syms_in_market:
            raise ValueError("sym is invalid for this market")


    def get_sym_list(self, verbose=False):
        self.syms_in_market = gen_pairs(self.market_function)
        if verbose: print(self.syms_in_market)

    def set_data_type(self, data_type):
        if data_type == 'trades':
            self.data_type = TRADES
            self.data_type_db = TradeInflux

        elif data_type == 'ticker':
            self.data_type = TICKER
            self.data_type_db = []
        elif data_type == 'book':
            self.data_type = L2_BOOK
            self.data_type_db = []
        else: raise ValueError("Data type not recognised")

    def add_item(self):
        try:
            self.feed_handler
        except:
            self.feed_handler = FeedHandler()

        self.feed_handler.add_feed(self.market(pairs=[self.sym], channels=[self.data_type],
                               callbacks={self.data_type: self.data_type_db(self.localhost,self.db_name)}))

    def define_item(self, market, sym, data_type):
        self.set_market(market)
        self.set_sym(sym)
        self.set_data_type(data_type)
        self.add_item()

    def run(self):
        self.feed_handler.run()






if __name__ == '__main__':

    md = getMarketData()


    # md.define_item(market='coinbase', sym='BTC-USD', data_type='trades')
    # md.define_item(market='binance', sym='BTC-USDT', data_type='trades')
    #
    # md.run()






    ######################## print list of traded syms
    md.set_market(market='binance')
    md.get_sym_list(verbose=True)

    #########################basic item creation structure
    # md.set_market(market='binance')
    # md.set_sym(sym='BTC-USDT')
    # md.set_data_type(data_type='trades')
    # md.add_item()

    sym =md.syms_in_market










