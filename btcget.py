# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>


import argparse
import yaml
import sys
from pathlib import Path
from abc import ABC, abstractmethod
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class BtcApi(ABC):

    @abstractmethod
    def get_btc_price(self):
        pass


class CoinMarketApi(BtcApi):
    def __init__(self, api_key, currency="USD"):
        self.api_key = api_key
        self.api_endpoint = "/v1/cryptocurrency/listings/latest"
        self.api_url = "https://pro-api.coinmarketcap.com" + self.api_endpoint
        self.api_header = "X-CMC_PRO_API_KEY"
        self.headers = {
            "Accepts": "application/json",
            self.api_header: api_key,
        }

        self.api_parameters = {
            "start": "1",
            "limit": "1",
            "convert": currency
        }


    def get_btc_price(self):
        try:
            response = requests.get(self.api_url, 
                                    headers=self.headers, 
                                    params=self.api_parameters)
            
            # data = json.loads(response.text)
            data = response.json()
            btc_price = data["data"][0]["quote"]["USD"]["price"]
            return round(btc_price, 2)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


API_BACKENDS = {
    "coinmarket": CoinMarketApi
}

class ApiBackendFactoryError:
    pass

class ApiBackendFactory:
    @staticmethod
    def create_backend(backend, api_key, currency="USD"):
        if backend in API_BACKENDS:
            return API_BACKENDS[backend](api_key, currency)
        else:
            raise ApiBackendFactory("Unsupported API backend:", backend)


def load_config(config_path):
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)
    
def save_config(config_path, api_backend, api_key, currency):
    with open(config_path, "w") as config_file:
        config_file.write(
            yaml.safe_dump({
            "api_backend": api_backend,
            "api_key": api_key,
            "currency": currency
        }))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reconfig", action="store_true", help="Re-configure api key and backend")
    args = parser.parse_args()

    config_path = Path.joinpath(Path.home(), ".btcget")
    if config_path.is_file():
        config = load_config(config_path)
        api_backend = config["api_backend"]
        api_key = config["api_key"]
        currency = config["currency"]
    else:
        try:
            api_backend = input("Enter API backend[coinmarket]: ")
            api_key = input("Enter API key: ")
            currency = input("Enter currency[USD]:")
        except KeyboardInterrupt:
            sys.exit(0)
        
        save_config(config_path, api_backend, api_key)

    api_backend = ApiBackendFactory.create_backend(api_backend, api_key, currency)
    sys.stdout.write("{:,}\n".format(api_backend.get_btc_price()))

if __name__ == "__main__":
    main()
