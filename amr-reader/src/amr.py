'''
 Return amr_table
'''

import os
import raw
import reader
import ne
import path
import nequery

'''
 Input: path of the directory of raw AMR files
'''
def get_amr_table_path(input_path):
    amr = ''
    if input_path[-1] != '/':
        input_path += '/'
    for i in os.listdir(input_path):
        tmp = open(input_path + i, 'r').read()
        amr += raw.wrap(tmp)
        print 'END OF FILE: %s' % i

    amr_table = reader.main(amr)
    ne.add_named_entity(amr_table)
    nequery.main(amr_table)
    return amr_table

'''
 Input: String of raw AMR
'''
def get_amr_table_str(input_str):
    amr = raw.wrap(input_str)
    amr_table = reader.main(amr)
    ne.add_named_entity(amr_table)
    nequery.main(amr_table)
    return amr_table
