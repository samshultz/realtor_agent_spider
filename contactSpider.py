import scrapy


class ContactSpider(scrapy.Spider):
    # name of the spider
    name = "contacts"
    # the url to start scraping from
    start_urls = [
        "https://www.realtor.com/realestateagents/Los-Angeles_CA"
    ]


    def parse(self, response):
        # check the page for the name of the agent...
        for href in response.css("div[itemprop=name] a::attr(href)"):
            # ...click on it and call the parse_agent method on each one
            yield response.follow(href, self.parse_agent)

        # follow pagination links...
        # for href in response.css("a.next::attr(href)"):
        #     #...repeat this method (parse method) on each page
        #     yield response.follow(href, self.parse)

    def parse_agent(self, response):
        # get the element containing the address info and extract the text
        address = response.css("#modalcontactInfo span[itemprop=streetAddress]::text").extract_first()
        # check if the address is available...
        if address is not None:
            # ... if it is, get the city, state and zipcode from it (this info
            # is contained in the last three info in the address)
            city, state, zipcode = address.split(",")[-3:]
            # separate the address
            addr = ''.join(address.split(",")[:-3])
        else:
            # if the address is not available
            # set the city, state, addr and zipcode to empty string
            city, state, zipcode = "", "", ""
            addr = ""

            # return a dictionary of the extracted info
        yield {
            "name": response.css("#modalcontactInfo p.modal-agent-name::text").extract_first().split(",")[0],
            "location": response.css("#modalcontactInfo p.modal-agent-location::text").extract_first().strip(),
            "address": addr,
            "city": city,
            "state": state,
            "zipcode": zipcode,

        }
