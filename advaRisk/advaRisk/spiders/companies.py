import scrapy
from bs4 import BeautifulSoup
import re
from advaRisk.items import ColConversion


class CompaniesSpider(scrapy.Spider):
    # spider name
    name = "companies"
    # allowed domains provided here
    allowed_domains = ["www.zaubacorp.com"]
    # we pass headers specifically user-agent as browser to avoid bot
    user_agent = 'Mozilla/5.0'

    # initiate the request
    def start_requests(self):
        """
            Scrapy will start execution from this method
        """
        yield scrapy.Request(url='https://www.zaubacorp.com/company-list/p-1-company.html',
                             callback=self.parse,
                             headers={'User-Agent': self.user_agent}
                             )

    def parse(self, response):
        """
            This method will call all company individual urls 
            and then move to next page util final page
            Params:
                response: its scrapy.request object that contains the scraped output
        """
        company_urls = response.xpath('//table//a/@href').getall()
        for url in company_urls:
            yield response.follow(url=url,
                                  callback=self.main,
                                  headers={'User-Agent': self.user_agent}
                                  )
        page = int(response.url.split('-')[-2])+1
        if page <= 13333:
            url = f'https://www.zaubacorp.com/company-list/p-{page}-company.html'
            yield response.follow(url=url,
                                  callback=self.parse,
                                  headers={'User-Agent': self.user_agent}
                                  )

    def getCompanyinfo(self, soup: BeautifulSoup):
        """
            This method will pick all the data related to company info
            and return it to the main method
            Params: 
                soup: its a BeautifulSoup parser for accessing HTML
            return : we return dictionary containing desired data
        """
        item = dict()
        key_values = ColConversion()
        if not soup.find('p', text=re.compile('CIN', re.I)):
            return None
        for key, value in key_values.cols.items():
            temp = soup.find('p', text=re.compile(key, re.I))
            item[value] = temp.find_next(
                'p').text.strip().lower() if temp else None
        temp = soup.find('p', text=re.compile('RoC-', re.I))
        item['roc'] = temp.text.split('-')[-1].lower() if temp else None
        return item

    def getAddressinfo(self, soup: BeautifulSoup, url: str):
        """
            This method will pick all the address data of the company and
            return output to the main method
            Params: 
                soup: its a BeautifulSoup parser for accessing HTML
                url: its the url that contains company info
            return : we return dictionary containing desired data
        """
        address_data = soup.find('p', text=re.compile(
            'Address:', re.I)).find_next('p').text.split(', ')
        sec_address = address_data[-1].split(' ')
        country_code = sec_address[-1]
        zipcode = sec_address[-2]
        state = sec_address[-3]
        if [x for x in address_data if 'city' in x.lower()]:
            city = ' '.join(sec_address[-5:-3])
        else:
            city = sec_address[-4]
        if len(address_data) == 1:
            address_1 = ' '.join(sec_address[:-4])
        else:
            address_1 = ' '.join(address_data[:-1])
        email = soup.find('b', text=re.compile('Email', re.I)).find_previous(
            'p').text.replace('Email ID:', '').strip()
        return {
            'address_1': address_1.lower(),
            'city': city.lower(),
            'state': state.lower(),
            'zipcode': zipcode.lower(),
            'country_code': country_code.lower(),
            'email': email.lower(),
            'info_url': url.lower(),
        }

    def getDirectorinfo(self, soup: BeautifulSoup):
        """
            This method will pick all the company director(s) data and
            return output to the main method
            Params: 
                soup: its a BeautifulSoup parser for accessing HTML
            return : we return dictionary containing desired data
        """
        unfilt_cols = []
        for each in soup.find_all('tr', {'data-parent': '#OrderPackages'}):
            unfilt_cols.extend([x.text.strip()
                                for x in each.find_all('p') if x.text.strip() != ''])
        return [
            {
                'did': unfilt_cols[i].lower(),
                'dname': unfilt_cols[i+1].lower(),
                'designation': unfilt_cols[i+2].lower(),
                'appointed_date': unfilt_cols[i+3].lower(),
            } for i in range(0, len(unfilt_cols), 5)
        ]

    def main(self, response):
        """
            This method will pick all data from above methods and
            produces the output to the database
            Params: 
                 response: its scrapy.request object that contains the scraped output
            return: it returns the desired output in dictionary format to DB
        """
        url = response.url
        soup = BeautifulSoup(response.text, 'lxml')
        company = self.getCompanyinfo(soup)
        if not company:
            return
        company['company_address'] = self.getAddressinfo(soup, url)
        company['company_director'] = self.getDirectorinfo(soup)
        yield company
