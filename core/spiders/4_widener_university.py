import scrapy
import re


from w3lib.html import remove_tags
from itemloaders import ItemLoader
from core.items import CustomItem, duration_cleaner


class WUSPider(scrapy.Spider):
    name = "wu"

    file_name = "Widener University"


    start_urls = [
        "https://www.widener.edu/academics/explore-programs?program_type=All&program_areas_interest=All&school=All"
    ]



    def parse(self, response):
        urls = response.xpath("//div[contains(@class, 'column')]//li//a/@href").getall()
        for url in urls[1:]: # first url is academics
            yield response.follow(url, callback=self.parse1)

   
    
    def parse1(self, response):
        il = ItemLoader(item=CustomItem(), selector=response)

        
        il.add_value("course_website", response.url)
        il.add_xpath("degree", "//div[contains(@class, 'eyebrow')]")
        il.add_xpath("study_mode", "//div[contains(@class, 'ataglance') and contains(./span, 'Format')]//div")
        il.add_xpath("course_name", "//h1")
        il.add_xpath("city", "//div[contains(@class, 'ataglance') and contains(./span, 'Location')]//ul//li")
        il.add_xpath("college", "//div[contains(@class, 'ataglance') and contains(./span, 'College')]//ul//li")

        il.add_xpath("credit_hours", "//div[contains(@class, 'ataglance') and contains(./span, 'Credit')]//p")

        il.add_xpath("course_des", "//section[contains(@id, 'program-overview')]//div[contains(@class, 'columns')]/*[not(self::div)]")
        il.add_xpath("course_des_html", "//section[contains(@id, 'program-overview')]//div[contains(@class, 'columns')]/*[not(self::div)]")
        
        il.add_xpath("career", "//section[contains(@id, 'career')]")
        il.add_xpath("career_html", "//section[contains(@id, 'career')]")

        il.add_xpath("course_struct", "//section[contains(@id, 'overview')]//div[contains(@id, 'expandables')]")
        il.add_xpath("course_struct_html", "//section[contains(@id, 'overview')]//div[contains(@id, 'expandables')]")

        il.add_xpath("other_requirements", "//section[contains(@id, 'admission')]")
        il.add_xpath("other_requirements_html", "//section[contains(@id, 'admission')]")

        fee_int = response.xpath("//span[contains(@class, 'tuition-card--header') and contains(., '$')]").get()
        if fee_int:
            il.add_value("fee", fee_int)
            il.add_value("fee_int", fee_int)
            il.add_value("fee_term", "Credit Hours")
            il.add_value("fee_year", "2025")
            il.add_value("fee_currency", "USD")

        duration = response.xpath("//div[contains(@class, 'ataglance') and contains(./span, 'Time to')]//p").get()
        if duration:
            il.add_value("duration_raw", duration)
            il.add_value("duration", duration)
            il.add_value("duration_term", duration)

        yield il.load_item()

  
