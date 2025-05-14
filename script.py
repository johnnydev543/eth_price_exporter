import time, os
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import requests
import json
from datetime import datetime

# URL_ETH_PRICE = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
URL_BINANCE_ETH_PRICE = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
URL_BINANCE_USDT_APR  = "https://www.binance.com/bapi/margin/v1/friendly/flexibleLoan/isolated/new/config/coinConfig?collateralCoin=USDT&loanCoin=USDT"

class DataCollector(object):

    def collect(self):

        eth_price_metric = GaugeMetricFamily(
            'eth_usd',
            'ETHUSD price',
            labels=['exchange']
        )

        usdt_apr_metric = GaugeMetricFamily(
            'usdt_marketApr',
            'USDT Savings Market APR',
            labels=['exchange']
        )

        usdt_loan_annualInterestRate = GaugeMetricFamily(
            'usdt_loan_annualInterestRate',
            'USDT laon Annual Interest Rate',
            labels=['exchange']
        )

        session = requests.Session()

        try:
            response = session.get(URL_BINANCE_ETH_PRICE, timeout=3)
            if response.ok:
                # price = response.json()['ethereum']['usd']
                eth_price = response.json()['price']
                eth_price_metric.add_metric(['binance'], eth_price)
                # print(eth_price)
        except requests.exceptions.ConnectionError:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), "Except: ConnectionError")
            time.sleep(300)
        except requests.exceptions.ConnectTimeout:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), "Except: ConnectTimeout")
            time.sleep(60)

        try:
            response = session.get(URL_BINANCE_USDT_APR, timeout=3)
            if response.ok:
                marketApr = response.json()['data']['collateralConfig'].get('marketApr')
                annualInterestRate = response.json()['data']['loanConfig'].get('annualInterestRate')
                # print(marketapr)
                usdt_apr_metric.add_metric(['binance'], marketApr)
                usdt_loan_annualInterestRate.add_metric('binance', annualInterestRate)
        except requests.exceptions.ConnectionError:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), "Except: ConnectionError")
            time.sleep(60)
        except requests.exceptions.ConnectTimeout:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), "Except: ConnectTimeout")
            time.sleep(60)
            
        yield eth_price_metric
        yield usdt_apr_metric
        yield usdt_loan_annualInterestRate

if __name__ == "__main__":

    REGISTRY.register(DataCollector())
    start_http_server(5000)
    while True:
        time.sleep(10)
