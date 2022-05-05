from setuptools import setup

setup(
    name="hebrew_calendar",
    version="0.2.0",
    author="Gooz Nick",
    description="Hebrew calendar implementation",
    long_description="Computation of hebrew calendar and some more according to Maimonedes Zmanin, Kidush Hachodesh",
    url="https://github.com/gooznick/hebrew_calendar",
    keywords="calendar",
    python_requires=">=3.6",
    install_requires=[""],
    extras_require={
        "test": ["pytest"],
    },
)
