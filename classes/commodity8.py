import requests
import os
from dotenv import load_dotenv


class Commodity8(object):
    def __init__(self, commodity_code, description=None):
        self.get_config()
        self.commodity_code = commodity_code
        self.productline_suffix = ""
        self.description = description

    def get_config(self):
        load_dotenv('.env')
        self.remote_url = os.getenv('REMOTE_URL')

    def gnid_pls(self):
        return self.commodity_code + "-" + self.productline_suffix

    def download(self):
        folder = os.path.join(os.getcwd(), "html")
        offset = 0
        print(self.commodity_code)
        proceed = True
        while proceed:
            filename = self.commodity_code + "-" + str(offset).zfill(4) + ".html"
            filepath = os.path.join(folder, filename)
            page_size = 25
            url = self.remote_url.format(
                offset=str(offset * page_size),
                commodity=self.commodity_code
            )
            response = requests.get(url)
            response_text = response.text
            with open(filepath, 'w') as f:
                f.write(response_text)
            if "Next</a>" in response_text:
                proceed = True
                offset += 1
            else:
                proceed = False
