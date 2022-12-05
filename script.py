import time, os
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server
import requests
import json
from datetime import datetime

URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

class CoingeckoAPICollector(object):

    def collect(self):

        price_metric = GaugeMetricFamily(
            'eth_usd',
            'ETHUSD price',
            labels=['exchange']
        )

        session = requests.Session()
        for _ in range(3):
            try:
                response = session.get(URL, timeout=3)
                if response.ok:
                    price = response.json()['ethereum']['usd']
                    price_metric.add_metric(['coingecko'], price)

            except requests.exceptions.ConnectTimeout:
                now = datetime.now()
                print(now.strftime("%d/%m/%Y %H:%M:%S"), "Failed to request")
                time.sleep(12)

        yield price_metric

if __name__ == "__main__":

    REGISTRY.register(CoingeckoAPICollector())
    start_http_server(5000)
    while True:
        time.sleep(10)
