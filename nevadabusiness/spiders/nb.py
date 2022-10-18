import scrapy


class NbSpider(scrapy.Spider):
    name = 'nb'
    allowed_domains = ['www.nevadabusiness.com']
    start_urls = ['https://www.nevadabusiness.com/nbm-business-directory/?wpbdp_view=all_listings']

    def parse(self, response):
        businesses =  response.css('div.listing-title>h3>a::attr(href)').extract()
        for business in businesses:
            url = business
            yield scrapy.Request(url, callback=self.parse_urls)

        next_page = response.css('span.next>a::attr(href)').get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_urls(self, response):
        BusinessName = response.css('a.main-title::text').get()
        try:
            Name = response.xpath('//span[text()="Contact Name, Title"]/following-sibling::div/text()').get()
            try:
                Names,title = response.xpath('//span[text()="Contact Name, Title"]/following-sibling::div/text()').get().split(',')
                try:
                    first, last = Names.split(' ')
                except:
                    first, middle, last = Names.split(' ')
            except:
                Names = response.xpath('//span[text()="Contact Name, Title"]/following-sibling::div/text()').get()
                try:
                    name,other = Names.split('-')
                    try:
                        first,last = name.split(' ')
                    except:
                        first, middle, last = name.split('')
                except:
                    try:
                        first, last = Names.split(' ')
                    except:
                        first, middle, last = Names.split(' ')
        except:
            first, last = '',''
        Address = response.xpath('//span[text()="*Address"]/following-sibling::div/text()').get()
        City = response.xpath('//span[text()="*City"]/following-sibling::div/text()').get()
        State = response.xpath('//span[text()="*State"]/following-sibling::div/text()').get()
        Zip = response.xpath('//span[text()="*Zipcode"]/following-sibling::div/text()').get()
        Email = response.xpath('//span[text()="Contact Email"]/following-sibling::div/text()').get()
        Phone = response.xpath('//span[text()="Phone"]/following-sibling::div/text()').get()

        yield{
            'Business Name': BusinessName,
            'First Name': first,
            'Last Name': last,
            'Address': Address,
            'City': City,
            'State': State,
            'Zip Code': Zip,
            'Email': Email,
            'Phone': Phone
        }

