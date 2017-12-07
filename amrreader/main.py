import os
import sys
import re
import argparse
import logging
from src import reader
from src import ne
from src import producer
from src import path


logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'AMR Reader'
    parser.add_argument('indir', help='directory to AMR input files')
    parser.add_argument('outdir', help='outpu directory')
    parser.add_argument('-g', '--graph',
                        help='generate AMR graphs -g=n: standard graphs \
                        -g=s: simplified graphs ', type=str)
    parser.add_argument('-n', '--node',
                        help='generate AMR nodes', action='store_true')
    parser.add_argument('-p', '--path',
                        help='generate AMR paths', action='store_true')
    parser.add_argument('-e', '--entity',
                        help='generate named entities', action='store_true')
    parser.add_argument('-v', '--visualization',
                        help='generate html visualization \
                        -v=n standard graphs -v=s: simplified graphs', type=str)

    args = parser.parse_args()
    indir = args.indir
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    for i in os.listdir(indir):
        logger.info('processing %s' % i)
        raw_amrs = open('%s/%s' % (indir, i), 'r').read()

        # Read raw AMR and add named entities
        sents = reader.main(raw_amrs)
        ne.add_named_entity(sents)

        if args.graph == 'n':
            producer.get_graph(sents, outdir)

        if args.graph == 's':
            producer.get_graph(sents, outdir, curt=True)

        if args.node:
            producer.get_node(sents, outdir)

        if args.entity:
            producer.get_namedentity(sents, outdir)

        if args.path:
            path.main(sents)
            producer.get_path(sents, outdir)

        if args.visualization == 'n':
            producer.get_html(sents, 'visualization', outdir)

        if args.visualization == 's':
            producer.get_html(sents, 'visualization', outdir, curt=True)
