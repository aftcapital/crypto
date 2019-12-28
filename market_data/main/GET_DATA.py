from src.getMarketData import getMarketData
import src.util as util
util.set_logging()






md = getMarketData()
md.define_item(market='binance', sym='BTC-USDT', data_type='trades')
md.define_item(market='binance', sym='ETH-USDT', data_type='trades')
md.run()




