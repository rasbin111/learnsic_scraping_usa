from logging import raiseExceptions
import scrapy
import re


from itemloaders import ItemLoader
from core.items import CustomItem


class UOWSSPider(scrapy.Spider):
    name = "uows"

    file_name = "University of Wiscinson-Superior"

    start_urls = [
        "https://www.uwsuper.edu/academics/undergraduate-programs/",
        "https://www.uwsuper.edu/academics/graduate-programs/",
    ]

    def parse(self, response):
        courses = response.xpath("//div[contains(@class, 'program-item')]")
        for course in courses:
            course_info = {}
            url = course.xpath(".//h3/a/@href").get()
            study_mode = course.xpath(".//span[contains(., 'Delivery')]/strong/text()").get()
            if study_mode:
                course_info["study_mode"] = study_mode
            yield response.follow(url, callback=self.parse1, meta={
                "course_info": course_info
            })
    
    def parse1(self, response):
        il = ItemLoader(item=CustomItem(), selector=response)

        course_info = response.meta.get("course_info")

        for key, value in course_info.items():
            il.add_value(key, value)
        
        il.add_value("course_website", response.url)
        duration = response.xpath("//a[contains(., 'Sample') and contains(., 'Plan')]/text()")
        if duration:
            il.add_value("duration_raw", duration)
            il.add_value("duration", duration)
            il.add_value("duration_term", duration)
        il.add_xpath("course_name", "//h1")

        il.add_xpath("course_des", "//div[contains(., 'Overview')] | //div[contains(@id, 'overview')]")
        il.add_xpath("course_des_html", "//div[contains(., 'Overview')] | //div[contains(@id, 'overview')]")

        il.add_xpath("career", "//h2[contains(@id, 'career')]/following-sibling::*")
        il.add_xpath("career_html", "//h2[contains(@id, 'career')]/following-sibling::*")

        program_url = response.xpath("//a[contains(., 'Required Courses')]/@href")

        

        yield response.follow(program_url, callback=self.parse2, meta = {
            "il": il
            })

    def parse2(self, response):
        il = response.meta.get("il")

        








