from scraper.common import ScrapeResult, Scraper, ScraperFactory


class LdlcScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.select_one('h1.title-1')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('div.price > div.price').get_text()
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'

        # check for add to cart button
        tag = self.soup.body.select_one('div.add-to-cart-bloc')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'
        else:
            self.alert_subject = f'Maybe {alert_subject}'
            self.alert_content = f'{alert_content.strip()}\n{self.url}'

@ScraperFactory.register
class LdlcScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'ldlc'

    @staticmethod
    def get_driver_type():
        return 'lean_and_mean'

    @staticmethod
    def get_result_type():
        return LdlcScrapeResult
