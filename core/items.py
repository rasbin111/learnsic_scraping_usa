
import scrapy
import re
from itemloaders.processors import MapCompose, TakeFirst, Join, Compose
from w3lib.html import remove_tags, remove_tags_with_content, replace_entities, strip_html5_whitespace
from html2text import HTML2Text

from libs.numbers import numbers_dict
from libs.months import months

def ielts_score_cleaner(item):
    match = re.search(r"\[(.*)\]", item)
    if match:
        return match.group(1)
    else:
        return item

def fee_cleaner(item):
    match = re.search(r"£\s*(\d+\,?\d+)", item)
    if match:
        return match.group(1)
    else:
        match = re.search(r"(\d+\,?\d+)", item)
        if match:
            return match.group(1)
        else:
            return item

# def duration_cleaner(item):
#     match = re.search(r"(\d+\.?\d*\-?\d*\.?\d*)", item)
#     if match:
#         value = match.group(1)
#         if "-" in value:
#             return value.split("-")[1]
#         else:
#             return value
#     else:
#         return item

def duration_cleaner(item):
    try:
        # for key, value in numbers_dict.items():
        #     if key in item:
        #         return value

        """ general """
        # match = re.search(r"\s*(\d+\.?\d*)", item)
        # if match:
        #     matched_value = match.group(1)
        #     return matched_value
        # else:
        #     return item
        
        """ Queens Mary University"""
        match = re.search(r"\|\s*(\d+\.?\d*)", item)
        if match:
            matched_value = match.group(1)
            return matched_value
        else:
            match = re.search(r"\s*(\d+\.?\d*)", item)
            if match:
                matched_value = match.group(1)
                return matched_value
            else:
                return item

        """ teeside university """
        # match = re.search(r"Length:\s*(\d+\.?\d*)", item)
        # if match:
        #     matched_value = match.group(1)
        #     return matched_value
        # else:
        #     return item
    except:
        return item

def duration_term_cleaner(item):
    
    """ general """
    try:
        item = item.lower()
        if "year" in item:
            return "year"
        elif "month" in item:
            return "month"
        elif "week" in item:
            return "week"
        elif "day" in item:
            return "day"
        elif "credit" in item:
            return "credit"
        else:
            return "year"
    except:
        pass


def remove_sup(item):
    return remove_tags_with_content(item, which_ones=["sup"])

def remove_h2(item):
    return remove_tags_with_content(item, which_ones=["h2"])

def remove_a(item):
    return remove_tags_with_content(item, which_ones=["a"])

def remove_img(item):
    return remove_tags_with_content(item, which_ones=["img"])

def remove_button(item):
    return remove_tags_with_content(item, which_ones=("button", ))

def remove_button_tag(item):
    return remove_tags(item, which_ones=("button", ))

def remove_figure(item):
    return remove_tags_with_content(item, which_ones=["figure"])

def strip_item(item):
    return item.strip()

def remove_un_ws(item):
    return re.sub("\s+", " ", item)

def study_mode_cleaner(item):
    item_lower = item.lower()
    if ("online" in item_lower and ("on campus" in item_lower or "on-campus"in item_lower)) or "blended" in item_lower:
        return "Hybrid"
    elif "online" in item_lower or "external" in item_lower:
        return "Online"
    elif "on campus" in item_lower:
        return 'On-campus'
    else:
        return item

def study_load_cleaner(item):
    item_lower = item.lower()
    if ("blended" in item_lower) or ("full" in item_lower and "part" in item_lower):
        return "Both"
    elif "full" in item_lower:
        return "Full-time"
    elif "part" in item_lower:
        return "Part-time"
    else:
        return re.sub(r"\s+", " ", item)

def intake_day_cleaner(item):
    try:
        item = re.sub("View all key dates", "",item, flags=re.IGNORECASE)
        item = re.sub("\s\s+", ", ", item)
        item = re.sub("\d{4}", "", item)
        item = re.sub(" , ", ", ", item)
        return item
    except:
        return item

def intake_month_cleaner(item):
    try:
        intake_month = ""
        itl = item.lower()
        im = re.sub(r"\d*\s*", "", itl)
        for month in months:
            if itl in month and len(itl)>1:
                intake_month += month + ", "
        return intake_month.strip().rstrip(",")
    except:
        return item
    # match = re.search(r"\-(\d{2})\-", item)
    # if match:
    #     return months[match.group(1)]
    # else:
    #     return item
    # match = re.search(r"\s*\-\s*([a-zA-Z]{3})", item)
    # if match:
    #     return match.group(1)
    # else:
    #     return item

def remove_svg(item):
    try:
        item = remove_tags_with_content(item, which_ones=["svg"])
        return item
    except:
        return item

def remove_img(item):
    try:
        item = remove_tags(item, which_ones=["img"])
        return item
    except:
        return item

def remove_picture(item):
    try:
        item = remove_tags_with_content(item, which_ones=["picture"])
        return item
    except:
        return item

def remove_a(item):
    try:
        item = remove_tags_with_content(item, which_ones=["a"])
        return item
    except:
        return item

def remove_dl(item):
    try:
        item = remove_tags_with_content(item, which_ones=["dl"])
        return item
    except:
        return item

def remove_strong(item):
    try:
        item = remove_tags_with_content(item, which_ones=["strong"])
        return item
    except:
        return item

def html_to_text(item):
    try:
        h = HTML2Text()
        h.ignore_links = True
        return h.handle(item)
    except:
        return item

def degree_cleaner(item):
    return re.sub(r"\s\s+", " ", item)
    # try:
    #     dm = re.search(r"(\S+)", item)
    #     if dm:
    #         return dm.group(1)
    #     else:
    #         return item
    # except:
    #     return item

def custom_join(values):
    joined_str = ""
    for value in values:
        if len(value.strip()) > 0:
            joined_str += value + ", "
        else:
            continue
    # joined_str = joined_str.strip("Start in")
    joined_str = joined_str.strip(", ")
    joined_str = joined_str.strip(",")

    return joined_str

def course_name_cleaner(item):
    """ general """
    # try:
    #     return re.sub(r"\s\s+", " ", item).strip()
    # except:
    #     return item

    """ University of surrey """
    # try:
    #     item = re.sub(r"\s\s+", " ", item).strip()
    #     item = re.sub(r"\s*\—?\s*2025\s*entry", "", item)
    #     return item
    # except:
    #     return item

    """ Angila Ruskin University """
    try:
        item = re.sub(r"\s\s+", " ", item).strip()
        item = re.sub(r".*?graduate\s*\-\s*", "", item)
        return item
    except:
        return item

def fee_year_cleaner(item):
    """general"""
    try:
        fym = re.search(r"(\d+)", item)
        if fym:
            return fym.group(1)
        else:
            return item
    except:
        return item



def remove_hidden(item):
    try:
        return re.sub(r"hidden>", ">", item)
    except:
        return item
def remove_display_none(item):
    try:
        return re.sub(r"display:none;", "", item)
    except:
        return item

class CustomItem(scrapy.Item):
    course_name = scrapy.Field(input_processor=MapCompose(remove_tags, replace_entities, course_name_cleaner,  strip_item), output_processor=Join())
    course_des = scrapy.Field(input_processor=MapCompose(remove_img, remove_figure, remove_hidden, replace_entities, strip_item, remove_button, html_to_text), output_processor=Join())
    course_des_html = scrapy.Field(input_processor=MapCompose(remove_img, remove_figure, strip_item, replace_entities), output_processor=Join())
    college = scrapy.Field(output_processor=Join(separator=", "))

    city = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Compose(custom_join))
    intake_month = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Compose(custom_join))
    intake_month_raw = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Compose(custom_join))
    intake_day = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item, intake_day_cleaner), output_processor=Join(separator=", "))
    duration = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item, duration_cleaner), output_processor=TakeFirst())
    duration_raw = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=TakeFirst())
    study_mode = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item, study_mode_cleaner), output_processor=Join())
    study_load = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item, study_load_cleaner), output_processor=Join())
    study_load_raw = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())
    delivery = scrapy.Field(input_processor=MapCompose(strip_item, ), output_processor=Join())
    course_website = scrapy.Field(output_processor=Join())
    career = scrapy.Field(input_processor=MapCompose(remove_picture, remove_img, remove_figure, remove_img, html_to_text, strip_item), output_processor=Join(separator="\n"))
    career_html = scrapy.Field(input_processor=MapCompose(remove_picture, remove_img, remove_figure, remove_img, remove_svg, remove_hidden, strip_item), output_processor=Join())
    # admission_requirements = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    # admission_requirements_html = scrapy.Field(output_processor=Join())
    other_requirements = scrapy.Field(input_processor=MapCompose(remove_button_tag, remove_svg, html_to_text, strip_item), output_processor=Join())
    other_requirements_html = scrapy.Field(input_processor=MapCompose(remove_button_tag, remove_display_none, remove_hidden, remove_svg, strip_item), output_processor=Join())
    course_struct = scrapy.Field(input_processor=MapCompose(remove_svg, html_to_text, replace_entities, strip_item), output_processor=Join(separator="\n"))
    course_struct_html = scrapy.Field(input_processor=MapCompose(strip_item, remove_hidden, remove_display_none, remove_button_tag, remove_svg), output_processor=Join())

    prerequisites = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    learning_outcomes = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())

    duration_term = scrapy.Field(input_processor=MapCompose(remove_tags, duration_term_cleaner), output_processor=Join())

    degree = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item, degree_cleaner), output_processor=Join())
    degree_category = scrapy.Field(output_processor=Join())
    degree_eligibility = scrapy.Field(output_processor=Join())
    apply_month = scrapy.Field(output_processor=Join())
    apply_day = scrapy.Field(output_processor=Join())
    dom_only = scrapy.Field(output_processor=Join())
    fee = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    fee_dom = scrapy.Field(output_processor=Join())
    fee_int = scrapy.Field(input_processor=MapCompose(remove_tags, fee_cleaner, strip_item), output_processor=Join())
    fee_year = scrapy.Field(input_processor=MapCompose(remove_tags, fee_year_cleaner), output_processor=TakeFirst())
    fee_term = scrapy.Field(output_processor=TakeFirst())
    fee_currency = scrapy.Field(output_processor=TakeFirst())
    application_fee = scrapy.Field(output_processor=Join())
    
    elr = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())
    ielts = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())
    
    ielts_aoverall = scrapy.Field(output_processor=Join())
    ielts_reading = scrapy.Field(output_processor=Join())
    ielts_writing = scrapy.Field(output_processor=Join())
    ielts_listening = scrapy.Field(output_processor=Join())
    ielts_speaking = scrapy.Field(output_processor=Join ())

    toefl_pbt = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())

    toefl_pbt_aoverall = scrapy.Field(output_processor=Join())
    toefl_pbt_reading = scrapy.Field(output_processor=Join())
    toefl_pbt_writing = scrapy.Field(output_processor=Join())
    toefl_pbt_listening = scrapy.Field(output_processor=Join())
    toefl_pbt_speaking = scrapy.Field(output_processor=Join ())
    
    toefl_ibt = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())

    toefl_ibt_aoverall = scrapy.Field(output_processor=Join())
    toefl_ibt_reading = scrapy.Field(output_processor=Join())
    toefl_ibt_writing = scrapy.Field(output_processor=Join())
    toefl_ibt_listening = scrapy.Field(output_processor=Join())
    toefl_ibt_speaking = scrapy.Field(output_processor=Join ())

    pte = scrapy.Field(input_processor=MapCompose(remove_tags, strip_item), output_processor=Join())

    pte_aoverall = scrapy.Field(output_processor=Join())
    pte_reading = scrapy.Field(output_processor=Join())
    pte_writing = scrapy.Field(output_processor=Join())
    pte_listening = scrapy.Field(output_processor=Join())
    pte_speaking = scrapy.Field(output_processor=Join())
    
    duolingo_aoverall = scrapy.Field(output_processor=Join())
    eng_overall = scrapy.Field(output_processor=Join())
    eng_test = scrapy.Field(output_processor=Join())
    eng_reading = scrapy.Field(output_processor=Join())
    eng_listening = scrapy.Field(output_processor=Join())
    eng_speaking = scrapy.Field(output_processor=Join())
    eng_writing = scrapy.Field(output_processor=Join())
    language = scrapy.Field(output_processor=Join(separator=", "))
    scholarship = scrapy.Field(input_processor=MapCompose(remove_tags, replace_entities), output_processor=Join())
 
    course_meta = scrapy.Field(output_processor=Join())
    # key = scrapy.Field(output_processor=Join())
    # fee_link = scrapy.Field(output_processor=Join())
    # sub_category = scrapy.Field(output_processor=Join())
    # category = scrapy.Field(output_processor=Join())
    # degree_level = scrapy.Field(output_processor=Join())
