from logging import raiseExceptions
import scrapy
import re


from itemloaders import ItemLoader
from w3lib.html import remove_tags
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
            if "undergraduate" in response.url:
                course_info["degree"] = "Undergraduate"
            elif "graduate" in response.url:
                course_info["degree"] = "Postgraduate"

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
        
        il.add_xpath("course_name", "//h1")
        il.add_value("course_website", response.url)


        duration = response.xpath("//a[contains(., 'Sample') and contains(., 'Plan')]/text()").get()
        if duration:
            il.add_value("duration_raw", duration)
            il.add_value("duration", duration)
            il.add_value("duration_term", duration)

        il.add_xpath("course_des", "//div[contains(., 'Overview')] | //div[contains(@id, 'overview')]")
        il.add_xpath("course_des_html", "//div[contains(., 'Overview')] | //div[contains(@id, 'overview')]")

        il.add_xpath("career", "//h2[contains(@id, 'career')]/following-sibling::*")
        il.add_xpath("career_html", "//h2[contains(@id, 'career')]/following-sibling::*")

        il.add_xpath("course_struct", "//div[contains(@id, 'curriculum')]")
        il.add_xpath("course_struct_html", "//div[contains(@id, 'curriculum')]")

        il.add_value("intake_month", "July, November")
        il.add_value("intake_day", "July 1, November 15")

        try:
            degree = course_info["degree"]

        except Exception as e:
            degree = ""

        study_mode = course_info["study_mode"]
        if study_mode:
            if ("Online" in study_mode and "On-Campus" not in study_mode) and "Undergraduate" in degree:
                # pass
                il.add_value("ielts_aoverall", "6.5")
                il.add_value("toefl_ibt_aoverall", "80")
                il.add_value("duolingo_aoverall", "115")
            
            else:
                il.add_value("ielts_aoverall", "5.5")
                il.add_value("pte_aoverall", "47")
                il.add_value("toefl_pbt_aoverall", "500")
                il.add_value("toefl_ibt_aoverall", "61")
                il.add_value("duolingo_aoverall", "100")


        # program_url = response.xpath("//a[contains(., 'Required Courses')]/@href")
        yield il.load_item()

        



        








