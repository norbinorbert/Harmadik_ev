import csv
import re

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "lab1"
    file_name = "output.csv"

    def start_requests(self):
        url = "https://www.cs.ubbcluj.ro/magunkrol/a-kar-felepitese/magyar-matematika-es-informatika-intezet/"
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "email", "webpage", "page_ok", "cv", "address", "research"])

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # each professor has its own div, which contains 2 other divs, one for the image, other for text
        professors = response.xpath("//div[@style='margin-bottom: 15px; margin-right: 15px; width: 630px']")

        for professor in professors:
            # the text div that contains the info needed for the csv file
            text_info = professor.xpath(".//div[@style='vertical-align: middle; text-align: left; display: table-cell; "
                                        "padding-left: 12px; padding-right: 12px; width: 503px; border-top: 1px solid "
                                        "#dddddd; border-bottom: 1px solid #dddddd; border-right: 1px solid #dddddd; "
                                        "border-left: 1px solid #dddddd']")
            name = text_info.xpath("./text()[1]").get().strip()

            # since there could be more than 1 email, use regex
            email_text = text_info.xpath(".//text()[contains(., 'E-mail:')]").get()
            email = re.findall(r'[a-zA-Z0-9_.+-]+\[at][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
                               , email_text) if email_text else []
            email = [e.replace("[at]", "@") for e in email]

            # every professor could have a CV or webpage or neither, but not both
            cv = text_info.xpath(".//a[contains(text(), 'Curriculum Vitae')]/@href").get(default=None)
            webpage = None
            if cv is None:
                webpage = text_info.xpath(".//a/@href").get(default=None)

            address = text_info.xpath(".//text()[contains(., 'Cím:')]").get(default='').replace("Cím:", "").strip()
            research = (text_info.xpath(".//text()[contains(., 'Szakterület:')]")
                        .get(default='').replace("Szakterület:", "").strip())

            data = {
                "name": name,
                "email": ", ".join(email),
                "webpage": webpage,
                "page_ok": None,
                "cv": cv,
                "address": address,
                "research": research,
            }

            # if there is a webpage, check if it loads. If no webpage, just save info to CSV
            if webpage:
                yield scrapy.Request(url=webpage, callback=self.page_loaded,
                                     errback=self.page_loading_error, cb_kwargs=dict(data=data))
            else:
                self.write_to_csv(data)

            yield {"image_urls": professor.xpath(".//img/@src").getall()}

            if cv:
                yield {"file_urls": [cv]}

    def page_loaded(self, response, data):
        data["page_ok"] = response.status < 400
        self.write_to_csv(data)

    def page_loading_error(self, failure):
        data = failure.request.cb_kwargs["data"]
        data["page_ok"] = False
        self.write_to_csv(data)

    def write_to_csv(self, data):
        with open(self.file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([data["name"], data["email"], data["webpage"], data["page_ok"], data["cv"],
                             data["address"], data["research"]])
