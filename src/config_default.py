PARSER_DEFS = { 'date' :
                    {'parser_type'   : 'regex'
                    ,'regex'  : 'test'
                    ,'out'    : lambda m : m.group(0)
                    ,'key'   : 'date'
                    },
                'length' :
                    {'parser_type'  : 'lambda'
                    ,'fun'          : lambda i : len(i)
                    }
              }

