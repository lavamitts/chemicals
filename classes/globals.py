commodity_codes = {}
descendant_dict = {}

def _to_bool(s):
    try:
        s = int(s)
        if s == 0:
            return False
        else:
            return True
    except Exception as e:
        return False
