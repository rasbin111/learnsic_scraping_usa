import scrapy
import re


from itemloaders import ItemLoader
from core.items import CustomItem


class VWUSPider(scrapy.Spider):
    name = "vwu"

    file_name = "Virginia Wesleyan University"

    start_urls = [
            "https://www.vwu.edu/academics/graduate-programs/",
            "https://www.vwu.edu/academics/majors/",
    ]

    def parse(self, response):
        urls = response.xpath("//div[contains(@id, 'textcontainer')]//li//a[contains(@href, 'programs')]/@href").getall()
        for url in urls:
            course_info = {}
            yield response.follow(url, callback=self.parse1, meta={
                "course_info": course_info
            })
    
    def parse1(self, response):
        il = ItemLoader(item=CustomItem(), selector=response)


        
        il.add_value("course_website", response.url)
        il.add_xpath("course_name", "//h1")

        il.add_xpath("course_des", "//div[contains(@id, 'textcontainer')]//h2[contains(., 'Description')]/following-sibling::p[1]")
        il.add_xpath("course_des_html", "//div[contains(@id, 'textcontainer')]//h2[contains(., 'Description')]/following-sibling::p[1]")

        il.add_xpath("course_struct", "//div[contains(@id, 'textcontainer')]")
        il.add_xpath("course_struct_html", "//div[contains(@id, 'textcontainer')]")

        yield il.load_item()
