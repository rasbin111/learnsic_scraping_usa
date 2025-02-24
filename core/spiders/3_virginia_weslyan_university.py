import scrapy
import re


from w3lib.html import remove_tags
from itemloaders import ItemLoader
from scrapy.http import response
from core.items import CustomItem


class VWUSPider(scrapy.Spider):
    name = "vwu"

    file_name = "Virginia Wesleyan University"

    def start_requests(self):

        urls = [
                "https://www.vwu.edu/academics/graduate-programs/",
                "https://www.vwu.edu/academics/majors/",
        ]

        yield scrapy.Request(urls[0], callback=self.parse_pg)
        yield scrapy.Request(urls[1], callback=self.parse_ug)


    def parse_pg(self, response):
        urls = response.xpath("//a[contains(@class, 'btn-teal') and contains(., 'Learn')]/@href").getall()
        for url in urls:
            yield response.follow(url, callback=self.parse1)

    def parse_ug(self, response):
        urls = response.xpath("//th[a]//a/@href | //td[a and contains(@class, 'text-right')]//a/@href")
        for url in urls:

            yield response.follow(url, callback=self.parse2)
    
    def parse1(self, response):
        il = ItemLoader(item=CustomItem(), selector=response)


        
        il.add_value("course_website", response.url)
        il.add_xpath("course_name", "//h1/text()")

        il.add_xpath("course_des", "//section[contains(@class, 'degree-info')]")
        il.add_xpath("course_des_html", "//section[contains(@class, 'degree-info')]")

        il.add_xpath("course_struct", "//section[contains(@class, 'course-information')]")
        il.add_xpath("course_struct_html", "//section[contains(@class, 'course-information')]")

        il.add_xpath("career", "//section[contains(@class, 'career')]")
        il.add_xpath("career_html", "//section[contains(@class, 'career')]")

        duration = response.xpath("//section[contains(@class, 'degree-info')]//li[contains(./strong, 'Program')]").get()
        if duration:
            duration = remove_tags(duration).strip()
            il.add_value("duration_raw", duration)
            il.add_value("duration", duration)
            il.add_value("duration_term", duration)

        fee_int = response.xpath("//section[contains(@class, 'degree-info')]//li[contains(./strong, '$')]").get()
        if fee_int:
            fee_int = remove_tags(fee_int)
            il.add_value("fee", fee_int)
            il.add_value("fee_int", fee_int)
            il.add_value("fee_term", "Credit Hour")
            il.add_value("fee_year", "2025")
            il.add_value("fee_currency", "USD")
        
        il.add_xpath("credit_hours", "//section[contains(@class, 'degree-info')]//li[contains(., 'Total Degree')]//strong/text()")
        il.add_xpath("intake_month", "//section[contains(@class, 'degree-info')]//li[contains(., 'Next')]//strong/text()")


        yield il.load_item()

    def parse2(self, response):
        il = ItemLoader(item=CustomItem(), selector=response)


        course_name = response.xpath("//div[contains(@class, 'side-contact-info')]//p[contains(.//strong, 'Major')]").get()
        if course_name:
            course_name = remove_tags(course_name)
            course_name = re.sub(r"^.*?\:\s*", "", course_name)
            il.add_value("course_name", course_name)
        il.add_value("course_website", response.url)


        yield il.load_item()


