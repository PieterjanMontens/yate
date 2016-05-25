## Pieterjan Montens 2016
## https://github.com/PieterjanMontens

import re

class Parse:
    __text = None

    #################################### PUBLIC METHODS
    def __init__(self):
        return None

    def set_data(self,text):
        self.__text = text
        return None

    def use(self,df):
        if 'pre' in df:
            check_text = df['pre'](self.__text)
        else:
            check_text = self.__text

        if df['parser_type'] == 'lambda':
            return df['fun'](check_text)

        elif df['parser_type'] == 'regex_extract':
            reg = re.compile(df['regex'],re.DOTALL | re.I | re.M)
            match = re.search(reg, check_text)
            if match is None:
                return 'not_found'
            else:
                return df['out'](match)

        elif df['parser_type'] == 'regex_multi_extract':
            reg = re.compile(df['regex'],re.DOTALL)
            out = re.findall(reg, check_text)
            return df['out'](out)

        elif df['parser_type'] == 'regex_instring':
            reg = re.compile(df['regex'],re.I | re.S)
            match = re.search(reg, check_text)
            if match is None:
                return False
            return True

        else:
            raise Exception('unknown parser type')
