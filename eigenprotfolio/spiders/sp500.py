import scrapy

class SP500Spider(scrapy.Spider):
    name = "sp500"
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
    ]

    def parse(self, response):
        table = response.xpath('//table[@id="constituents"]')
        rows = table.xpath('.//tr')[1:]

        for row in rows:
            symbol = row.xpath('.//td[1]/a/text()').get()
            company = row.xpath('.//td[2]/a/text()').get()
            sector = row.xpath('.//td[4]/text()').get()

            yield {
                'symbol': symbol,
                'company': company,
                'sector': sector,
            }

