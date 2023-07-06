from bs4 import BeautifulSoup
from classes.cas_record import CasRecord


class HtmlFile(object):
    def __init__(self, filename, cas_specifics):
        self.cas_specifics = cas_specifics
        self.cas_records = []
        self.filename = filename
        f = open(self.filename, "r")
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        tables = soup.findAll('table', attrs={"class": "ecl-table"})
        if len(tables) > 0:
            table = tables[0]
            tbody = table.find('tbody')
            rows = tbody.findAll('tr')
            if len(rows) > 0:
                for row in rows:
                    cells = row.findAll('td')
                    cas_record = CasRecord(cells, self.cas_specifics)
                    self.cas_records.append(cas_record._as_list())
