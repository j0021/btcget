from setuptools import setup

setup(
    name="btcget",
    version="0.0.1",
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