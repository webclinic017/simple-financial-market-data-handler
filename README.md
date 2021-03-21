# Simply fetching and managing historical market data of key financial assets
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

So, to get a long term history without gaps the data must be fetched at least once a week (for one minute intervals). However, you can contact me at any time, I can provide individual history data since January 2021. I do not share this publicly to avoid legal issues.

To get a first impression about how the fetched data may be processed, please have a look at [this](https://github.com/neongelb/deep-financial-market-analysis).

## Overview
Utilizing this codebase allows to maintain a long-term collection of historical market data of currently approx. 1300 different symbols. I'll try to keep the index component symbols as up-to-date as possible. Thus, for you it's necessary to contuously pull updates from this repository.
### So far considered symbols:
- **Indizes**: 
  - USA: S&P 500, Dow Jones, Nasdaq-100 
  - Europe: DAX, MDAX, TECDAX, SDAX, CAC40, FTSE100, IBEX35, STOXX Europe 50, 
  - Asia: Nikkei 225, HSI, SSE Composite, CSI300
- **Stocks**: 
  - USA: S&P 500 Components, Dow Jones Components, Nasdaq-100 Components 
  - Europe: DAX Components, MDAX Components, TECDAX Components, SDAX Components
  - Asia: Nikkei 225 Components, HSI Components, CSI300 Components
- **Miscellaneous**:
  - Currencies: EUR-USD
  - Commodities: Gold
  - Cryptos: BTC-USD, ETH-USD, CMC Crypto 200 Index
  - ETFS: iShares MSCI World ETF
  - Others: Treasury Yield 10 Years

Feel free to propose any other relevant symbols available on Yahoo! finance.

## Getting Started
### Requirements
- [yfinance](https://github.com/ranaroussi/yfinance) >= 0.1.55

## License
This codebase is distributed under the **Apache Software License**. Please, see the [LICENSE](LICENSE) file for details.


## Acknowledgements
- [yfinance](https://github.com/ranaroussi/yfinance)




