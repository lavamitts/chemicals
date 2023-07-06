import classes.globals as g


class CasRecord(object):
    def __init__(self, cells, cas_specifics):
        self.cas_specifics = cas_specifics
        self.cells = cells
        self.process()
        self.get_specific_commodity_code()

    def process(self):
        self.cus = self.cleanse(self.cells[0].text).strip()
        self.cn_code = self.cleanse(self.cells[1].text).strip()
        self.cas_rn = self.cleanse(self.cells[2].text).strip()
        self.ec_number = self.cleanse(self.cells[3].text).strip()
        self.un_number = self.cleanse(self.cells[4].text).strip()
        self.nomen = self.cleanse(self.cells[5].text).strip()
        self.name = self.cleanse(self.cells[6].text).strip()
        self.cn_code_safe = None

    def get_specific_commodity_code(self):
        if self.cus == "0026260-2":
            a = 1
        if self.cas_rn in self.cas_specifics:
            found = False
            for item in self.cas_specifics[self.cas_rn]:
                if item[0:8] == self.cn_code:
                    found = True
                    self.cn_code_safe = self.cn_code
                    self.cn_code = item
                    break
            if not found:
                self.cn_code_safe = self.cn_code
                self.cn_code = self.cn_code + "00-80"
            a = 1
        else:
            # return
            lookup_values = []
            pls_list = ["10", "20", "30", "40", "50", "60", "70", "80"]
            for pls in pls_list:
                code_to_lookup = self.cn_code + "00-" + pls
                try:
                    test = g.commodity_codes[code_to_lookup]
                    found = True
                except Exception as e:
                    found = False
                    pass
                if found:
                    resolved = False
                    end_line = g._to_bool(g.commodity_codes[code_to_lookup].end_line)

                    if end_line:
                        self.cn_code_safe = self.cn_code
                        self.cn_code = g.commodity_codes[code_to_lookup].gnid_pls()
                    else:
                        try:
                            descendant_list = g.descendant_dict[code_to_lookup]
                            for descendant in descendant_list:
                                if g.commodity_codes[descendant].description.lower().strip() == "other":
                                    self.cn_code_safe = self.cn_code
                                    self.cn_code = descendant
                                    resolved = True
                                    break
                        except Exception as e:
                            found = False
                            print("No descendant list found for", code_to_lookup)
                        a = 1
                    if not resolved:
                        if found:
                            self.cn_code_safe = self.cn_code
                            self.cn_code = code_to_lookup
                    if found:
                        break

    def cleanse(self, s):
        if s is None:
            return ""
        else:
            s = s.replace("\n", "")
        return s

    def _as_dict(self):
        s = {
            "cus": self.cus,
            "cn_code": self.cn_code,
            "cas_rn": self.cas_rn,
            "ec_number": self.ec_number,
            "un_number": self.un_number,
            "nomen": self.nomen,
            "name": self.name
        }
        return s

    def _as_list(self):
        s = [
            self.cus,
            self.cn_code,
            self.cas_rn,
            self.ec_number,
            self.un_number,
            self.nomen,
            self.name
        ]
        return s
