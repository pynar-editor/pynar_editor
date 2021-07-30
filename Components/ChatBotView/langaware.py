class LanguageAwareStr(str):
    lang = None

class TurkishStr(LanguageAwareStr):
    lang = 'tr'
    _case_lookup_upper = {'İ': 'i', 'I': 'ı'}  # lookup uppercase letters
    _case_lookup_lower = {v: k for (k, v) in _case_lookup_upper.items()}

    # here we override the lower() and upper() methods
    def lower(self):
        chars = [self._case_lookup_upper.get(c, c) for c in self]
        result = ''.join(chars).lower()
        cls = type(self)  # so we return a TurkishStr result
        return cls(result)

    def upper(self):
        chars = [self._case_lookup_lower.get(c, c) for c in self]
        result = ''.join(chars).upper()
        cls = type(self)  # so we return a TurkishStr result
        return cls(result)