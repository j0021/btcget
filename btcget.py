# SPDX-License-Identifier: Unlicense

import argparse
import yaml
import sys
from pathlib import Path
from abc import ABC, abstractmethod
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

progver="0.0.5"

# ============= API Backends =============


class BtcApiFetchError(Exception):
    pass

class _BtcApi(ABC):

    @abstractmethod
    def get_btc_price(self):
        pass

    def fetch(self, api_url, api_headers, api_parameters):
        try:
            response = requests.get(api_url,
                                    headers=api_headers,
                                    params=api_parameters)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise BtcApiFetchError("Unable to connect to API URL") from None

        if response.status_code == 200:
            return response
        else:
            raise BtcApiFetchError("HTTP response was not 200 OK, got status: {}".format(response.status_code))

class CoinMarketApiError(Exception):
    pass

class CoinMarketApi(_BtcApi):
    def __init__(self, api_key: str, currency: str = "USD"):
        self.api_key = api_key
        self.currency = currency
        self.api_endpoint = "/v1/cryptocurrency/listings/latest"
        self.api_url = "https://pro-api.coinmarketcap.com" + self.api_endpoint
        self.api_header = "X-CMC_PRO_API_KEY"
        self.api_headers = {
            "Accepts": "application/json",
            self.api_header: api_key,
        }

        self.api_parameters = {
            "start": "1",
            "limit": "1",
            "convert": self.currency
        }


    def get_btc_price(self):
        response = self.fetch(self.api_url,
                                self.api_headers,
                                self.api_parameters)

        data = response.json()
        try:
            btc_price = data["data"][0]["quote"][self.currency]["price"]
        except KeyError:
            raise CoinMarketApiError("Unable to parse price data from") from None

        return round(btc_price, 2)


class ApiBackendFactoryError(Exception):
    pass


class ApiBackendFactory:
    @staticmethod
    def create_backend(backend, api_key: str, currency: str = "USD"):
        if backend == "coinmarket":
            return CoinMarketApi(api_key, currency)
        else:
            raise ApiBackendFactoryError("Unsupported API backend:", backend)


# ============= Config Loading =============

_config_path = Path.joinpath(Path.home(), ".btcget")
_default_backend = "coinmarket"
_default_currency = "USD"


class ConfigNotFound(Exception):
    pass

def load_config(config_path: Path = _config_path):
    if config_path.is_file():
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    else:
        raise ConfigNotFound("Config not found")


def _set_config(args):
    config = load_config(_config_path)
    if args.backend:
        config["backend"] = args.backend
    if args.key:
        config["key"] = args.key
    if args.currency:
        config["currency"] = args.currency
    _save_config(config)

def _save_config(config, config_path: Path = _config_path):
    with open(str(config_path), "w") as config_file:
        config_file.write(
            yaml.safe_dump(config)
        )
    sys.exit(0)

def _init_config(args):

    with open(str(_config_path), "w") as config_file:
        config_file.write(
            yaml.safe_dump(
                {
                    "backend": _default_backend,
                    "currency": _default_currency,
                    "key": ""
                }
            )
        )

    print("\nConfig initialized at {} with default backend/currency.".format(_config_path))
    print("\nAdd your API key with the command:\n")
    print("\tbtcget config --key <api key>\n")
    sys.exit(0)


def _main():
    parser = argparse.ArgumentParser(prog="btcget")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {}".format(progver))
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands")
    config_parser = subparsers.add_parser("config")
    config_parser.add_argument("--backend", type=str, help="API backend")
    config_parser.add_argument("--key", type=str, help="API key")
    config_parser.add_argument("--currency", type=str, help="Conversion currency")
    config_parser.set_defaults(func=_set_config)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("config", action="store_true", help="Create config with defaults")
    init_parser.set_defaults(func=_init_config)

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        pass

    config = load_config(_config_path)
    try:
        api_backend = ApiBackendFactory.create_backend(config["backend"],
                                                       config["key"],
                                                       config["currency"])
    except ConfigNotFound as e:
        sys.exit(1)

    print("{:,}".format(api_backend.get_btc_price()))

if __name__ == "__main__":
    _main()
