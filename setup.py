from setuptools import setup, find_packages

setup(
    name="ZTMAnalysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "jupyter"
    ],
    description="Tool for analyzing and predicting bus arrival times",
    author="MateuszAndruszkiewicz",
    license="MIT"
)