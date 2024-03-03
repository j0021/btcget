from setuptools import setup

with open("README.md") as f:
    doc = f.read()

setup(
    name="btcget",
    version="0.0.4",
    description="Simple REST API wrapper for fetching Bitcoin market price data via multiple backends.",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="Joel Torres",
    author_email="joel@torreshub.com",
    url="https://github.com/j0021/btcget",
    license="The Unlicense",
    platforms="any",
    py_modules=["btcget"],
    install_requires=[
        "PyYAML==6.0.1",
        "requests==2.31.0"
    ],
    entry_points={
        "console_scripts":[
            "btcget=btcget:_main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP"
    ]
)