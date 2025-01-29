from setuptools import setup, find_packages

setup(
    name="ZTMAnalysis",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "scikit-learn",
        "rich",
        "tqdm",
    ],
    description="Tool for analyzing and predicting bus arrival times",
    author="MateuszAndruszkiewicz",
    license="MIT"
)