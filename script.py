import time, os
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import requests
import json

URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

class BinanceAPICollector(object):

    def collect(self):

        price_metric = GaugeMetricFamily(
            'eth_usd',
            'ETHUSD price',
            labels=['exchange']
        )

        response = requests.get(URL)
        price = response.json()['ethereum']['usd']
        price_metric.add_metric(['coingecko'], price)

        yield price_metric

if __name__ == "__main__":

    REGISTRY.register(BinanceAPICollector())
    start_http_server(5000)
    while True:
        time.sleep(10)
