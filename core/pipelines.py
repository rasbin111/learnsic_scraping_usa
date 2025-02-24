from itemadapter import adapter
import scrapy
import pandas as pd

from itemadapter.adapter import ItemAdapter


class CustomItemPipeline:

    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        try:
            df.sort_values(by="course_name", axis=0,
                           inplace=True, ascending=True)
        except:
            pass
        df.to_excel(f"scraped_data/{spider.file_name}.xlsx", index=False)
        print("Item Exported Succesfully")


 
