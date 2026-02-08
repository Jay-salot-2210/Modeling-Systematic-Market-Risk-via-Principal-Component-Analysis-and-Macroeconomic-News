import scrapy
import pandas as pd
import time
from eigenprotfolio.eigenprotfolio.preprocessor_tickers import get_cleaned_tickers

class YahooBulkSpider(scrapy.Spider):
    name = "yahoo_prices"
    def start_requests(self):
        tickers = get_cleaned_tickers()

        for ticker in tickers:
            url =(
                    f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
                    f"?period1=1262304000"
                    f"&period2={int(time.time())}"
                    f"&interval=1d&events=history&includeAdjustedClose=true"
            )

            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={'ticker': ticker},
                dont_filter=True
            )
    def parse(self, response):
        ticker = response.meta['ticker']
        yield {
            'ticker': ticker,
            'csv': response.text,
        }