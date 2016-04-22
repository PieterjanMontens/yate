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
        if df['parser_type'] == 'lambda':
            return df['fun'](self.__text)
        elif df['parser_type'] == 'regex':
            reg = re.compile(df['regex'],re.DOTALL)
            match = re.search(reg, self.__text)
            if match is None:
                return 'not_found'
            else:
                return df['out'](match)
        else:
            raise Exception('unknown parser type')
