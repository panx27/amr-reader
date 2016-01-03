import os
import sys
import re
import argparse
from src import raw
from src import reader
from src import output
from src import ne
from src import path
from src import nequery

if __name__ == '__main__':
    ### Arguments
    parser = argparse.ArgumentParser()
    parser.description = 'AMR Reader'
    parser.add_argument('input', type=str,
                        help='directory of AMR files', nargs='+')
    parser.add_argument('output', type=str,
                        help='directory of output files', nargs='+')
    parser.add_argument('-g', '--graph',
                        help='output AMR graphs \
                        -g=n: normal graphs -g=s: simple graphs ', type=str)
    parser.add_argument('-n', '--node',
                        help='output AMR nodes', action='store_true')
    parser.add_argument('-p', '--path',
                        help='output AMR paths', action='store_true')
    parser.add_argument('-e', '--entity',
                        help='output named entities', action='store_true')
    parser.add_argument('-q', '--query',
                        help='output named entity queries', action='store_true')
    parser.add_argument('-v', '--visualization',
                        help='output html format visualization \
                        -v=n normal graphs -v=s: simple graphs', type=str)
    args = parser.parse_args()

    ### Output path
    output_path = args.output[0]
    if output_path[-1] != '/':
        output_path += '/'
    try: os.mkdir(output_path)
    except OSError: pass

    ### Input path
    input_path = args.input[0]
    if input_path[-1] != '/':
        input_path += '/'

    ### Wrap raw AMR
    amr = ''
    for i in os.listdir(input_path):
        tmp = open(input_path + i, 'r').read()
        amr += raw.wrap(tmp)
        print 'END OF FILE: %s' % i

    ### Generate amr_table
    amr_table = reader.main(amr)
    ne.add_named_entity(amr_table)

    ### Arguments Parser
    if args.graph == 'n':
        output.graph(amr_table, output_path)

    if args.graph == 's':
        output.graph(amr_table, output_path, curt=True)

    if args.node:
        output.node(amr_table, output_path)

    if args.entity:
        output.namedentity(amr_table, output_path)

    if args.path:
        path.main(amr_table)
        output.path(amr_table, output_path)

    if args.visualization == 'n':
        nequery.main(amr_table, chain=False)
        output.html(amr_table, 'visualization', output_path)

    if args.visualization == 's':
        nequery.main(amr_table, chain=False)
        output.html(amr_table, 'visualization', output_path, curt=True)

    if args.query:
        nequery.main(amr_table)
        output.query(amr_table, output_path)
