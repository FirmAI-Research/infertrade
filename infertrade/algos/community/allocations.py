"""
Functions used to compute allocations - % of your portfolio to invest in a market or asset.

Copyright 2021 InferStat Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created by: Joshua Mason
Created date: 11/03/2021
"""


import pandas as pd
from sklearn.preprocessing import FunctionTransformer
from infertrade.PandasEnum import PandasEnum


def fifty_fifty(dataframe) -> pd.DataFrame:
    """Allocates 50% of strategy budget to asset, 50% to cash."""
    dataframe["allocation"] = 0.5
    return dataframe


def buy_and_hold(dataframe) -> pd.DataFrame:
    """Allocates 100% of strategy budget to asset, holding to end of period (or security bankruptcy)."""
    dataframe[PandasEnum.ALLOCATION.value] = 1.0
    return dataframe


def constant_allocation_size(dataframe: pd.DataFrame, fixed_allocation_size: float = 1.0) -> pd.DataFrame:
    """
    Returns a constant allocation, controlled by the constant_position_size parameter.

    parameters:
    constant_allocation_size: determines allocation size.
    """
    dataframe[PandasEnum.ALLOCATION.value] = fixed_allocation_size
    return dataframe


def high_low_difference(dataframe: pd.DataFrame, scale: float = 1.0, constant: float = 0.0) -> pd.DataFrame:
    """
    Returns an allocation based on the difference in high and low values. This has been added as an
    example with multiple series and parameters

    parameters:
    scale: determines amplitude factor.
    """
    dataframe[PandasEnum.ALLOCATION.value] = (dataframe["high"] - dataframe["low"]) * scale + constant
    return dataframe

def sma_crossover_strategy(dataframe: pd.DataFrame,
    fast: int = 0,
    slow: int = 0) -> pd.DataFrame:
    """ A Simple Moving Average crossover strategy Crossover Strategy, buys when """
    # set price to dataframe price column
    price = dataframe["price"]
    # Compute Fast and Slow SMA 
    fast_sma = price.rolling(window = fast, min_periods = fast).mean()
    slow_sma = price.rolling(window = slow, min_periods = slow).mean()
    position = np.where(fast_sma  > slow_sma, 1.0, 0.0)
    dataframe.position = position

    return dataframe


infertrade_export_allocations = {
    "fifty_fifty": {
        "function": fifty_fifty,
        "parameters": {},
        "series": [],
        "available_representation_types": {
            "github_permalink": "https://github.com/ta-oliver/infertrade/blob/5aa01970fc4277774bd14f0823043b4657e3a57f/infertrade/algos/community/allocations.py#L28"
        },
    },
    "buy_and_hold": {
        "function": buy_and_hold,
        "parameters": {},
        "series": [],
        "available_representation_types": {
            "github_permalink": "https://github.com/ta-oliver/infertrade/blob/5aa01970fc4277774bd14f0823043b4657e3a57f/infertrade/algos/community/allocations.py#L34"
        },
    },
    "constant_allocation_size": {
        "function": constant_allocation_size,
        "parameters": {"fixed_allocation_size": 1.0},
        "series": [],
        "available_representation_types": {
            "github_permalink": "https://github.com/ta-oliver/infertrade/blob/5aa01970fc4277774bd14f0823043b4657e3a57f/infertrade/algos/community/allocations.py#L46"
        },
    },
    "high_low_difference": {
        "function": high_low_difference,
        "parameters": {"scale": 1.0, "constant": 0.0},
        "series": ["high", "low"],
        "available_representation_types": {
            "github_permalink": "https://github.com/ta-oliver/infertrade/blob/5aa01970fc4277774bd14f0823043b4657e3a57f/infertrade/algos/community/allocations.py#L57"
        },
    },
    "smaCrossoverStrategy": {
        "function": sma_crossover_strategy,
        "parameters": {
            "fast": 0,
            "slow": 0,
        },
        "series": ["price"],
        "available_representation_types": {
            "github_permalink": "" #TODO: add this after initial commit
        },
    },
}


def scikit_allocation_factory(allocation_function: callable) -> FunctionTransformer:
    """This creates a SciKit Learn compatible Transformer embedding the position calculation."""
    return FunctionTransformer(allocation_function)
