class Chemical(object):
    def __init__(self, formula, synonyms, cas_number):
        self.formula = self.cleanse(formula)
        self.synonyms = self.cleanse(synonyms)
        self.cas_number = self.cleanse(cas_number)

    def cleanse(self, s):
        if s is None:
            return ""
        else:
            s = s.replace("\n", "")
        return s

    def _as_dict(self):
        s = {
            "formula": self.formula,
            "synonyms": self.synonyms,
            "cas_number": self.cas_number
        }
        return s
