import os
import sys
import re
import argparse
from src import reader
from src import output
from src import ne
from src import path
from src import nequery

if __name__ == '__main__':
    ### Arguments
    parser = argparse.ArgumentParser()
    parser.description = 'AMR Reader'
    parser.add_argument('indir', type=str,
                        help='directory of AMR files', nargs='+')
    parser.add_argument('outdir', type=str,
                        help='directory of output files', nargs='+')
    parser.add_argument('-g', '--graph',
                        help='output AMR graphs \
                        -g=n: normal graphs -g=s: simplified graphs ', type=str)
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
                        -v=n normal graphs -v=s: simplified graphs', type=str)
    args = parser.parse_args()

    ### Output Dir
    outdir = args.outdir[0]
    try:
        os.mkdir(outdir)
    except OSError:
        pass

    ### Input Dir
    indir = args.indir[0]

    ### Merge raw AMR
    raw_amr = ''
    for i in os.listdir(indir):
        raw_amr += open('%s/%s' % (indir, i), 'r').read()
        print 'END OF FILE: %s' % i

    ### Read raw AMR
    amres = reader.main(raw_amr)
    ne.add_named_entity(amres)

    ### Arguments Parser
    if args.graph == 'n':
        output.graph(amres, outdir)

    if args.graph == 's':
        output.graph(amres, outdir, curt=True)

    if args.node:
        output.node(amres, outdir)

    if args.entity:
        output.namedentity(amres, outdir)

    if args.path:
        path.main(amres)
        output.path(amres, outdir)

    if args.query:
        nequery.main(amres)
        output.query(amres, outdir)

    if args.visualization == 'n':
        output.html(amres, 'visualization', outdir)

    if args.visualization == 's':
        output.html(amres, 'visualization', outdir, curt=True)
