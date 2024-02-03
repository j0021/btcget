from setuptools import setup
from btcget import __version__

setup(
    name="btcget",
    version=__version__,
    py_modules=["btcget"],
    install_requires=[
        "PyYAML==6.0.1",
        "requests==2.31.0"
    ],
    entry_points={
        "console_scripts":[
            "btcget=btcget:_main"
        ]
    }
)