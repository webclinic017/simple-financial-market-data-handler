# fetching-and-managing-major-financial-data
Code to automatically fetch and manage data of the most relevant indices, stocks and other financial assets utilizing yfinance.


## Introduction

[yfinance](https://github.com/ranaroussi/yfinance) is a great and well established python library to download historical market data from Yahoo! finance. This repository builds on this and additionally provides a continuously updated compilation of symbols for the most important stock indices, related components and other financial assets. Moreover, it allows to easily store and update fetched symbol data in [pandas](https://github.com/pandas-dev/pandas) dataframes on disk. Thus, you can obtain a comprehensive basis for stock market analysis and for development of trading algorithms with minimal effort.

**Note**: The Yahoo Finance API limits the number of requests per hour to 2000. This may become an issue if you seek to download data for each available symbol and interval at a single blow. In addition, the time period in which data can be retrieved retroactively is limited, depending on the selected interval size:

| interval  | max period |
| ------------- | ------------- |
| 1 min  | 7 days  |
| 15 min  | 60 days  |
| 60 min  | 730 days  |
| 1 day  | 10 years  |

So, to get a long term history without gaps the data must be fetched at least once a week (for one minute intervals).

To get a first impression about how the fetched data may be processed, please have a look at:

## Overview


## Installation
### Requirements


## Getting Started




