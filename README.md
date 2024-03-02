# btcget

Simple REST API wrapper for fetching Bitcoin market price data via multiple backends.

## Installation

```
pip install btcget
```

## Supported API Backends

* coinmarket (Coin Market API)

## Usage

1. Configure the backend, token, and currency converter (defaulting to "coinmarket" backend and "USD" currency):
```
btcget init
```

init will create a config file (.btcget) in your home directory, defaulting to (defaulting to "coinmarket" backend and "USD" currency). If these defaults are good for you, then you can simply add your API token for the backend:

```
btcget config --key <api key>
```

Otherwise, update your backend and currency converter:

```
btcget config --backend <api backend>
btcget config --currency <currency converter>
```
2. Run btcget to test fetching the current market price. This can also be used to pipe it to other programs for further processing.

```
btcget
```

3. Import to your application:

```
import btcget

config = btcget.load_config()

api_backend = btcget.ApiBackendFactory.create_backend(config["backend"],
                                                      config["key"],
                                                      config["currency"])

btc_market_price = api_backend.get_btc_price()
```

Steps 1 and 2 can be skipped and you can simply supply your arguments in your app to the backend creator. If using multiple apps, then steps 1 and 2 can help for having a common configuration.

