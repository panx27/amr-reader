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
 Input: path of the directory of AMR doc files
'''
def get_amr_table_path(input_path):
    raw_amr = list()
    for i in os.listdir(input_path):
        raw.read(input_path, i, raw_amr)
    raw_amr = ''.join(raw_amr)

    amr_table = reader.main(raw_amr)
    ne.add_named_entity(amr_table)
    nequery.main(amr_table)

    return amr_table

'''
 Input: String of raw AMR
'''
def get_amr_table_str(input_str):
    amr_table = reader.main(input_str)
    ne.add_named_entity(amr_table)
    nequery.main(amr_table)

    return amr_table
