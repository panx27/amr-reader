import os
import sys
import re
import get_raw_amr
import amr_reader
import amr_output

def usage():
    return 'Usage: python main.py <path of the directory of AMR files>'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.description = 'AMR Reader'
    parser.add_argument('directory', type=str, help='directory of AMR files', nargs='+') 
    parser.add_argument('-g', '--graph', help='output AMR graphs \'../output/graphs/\'', action='store_true')
    parser.add_argument('-n', '--node', help='output AMR nodes \'../output/amr_nodes\'', action='store_true')
    parser.add_argument('-p', '--path', help='output AMR paths \'../output/amr_paths\'', action='store_true')
    parser.add_argument('-e', '--entity', help='output named entities \'../output/nes\'', action='store_true')
    parser.add_argument('-q', '--query', help='output named entity queries \'../output/queries\'', action='store_true')
    parser.add_argument('-v', '--visualization', help='output html format visualization \'../output/*.html\'', action='store_true')
    args = parser.parse_args()

    output_path = '../output/'
    try: os.mkdir(output_path)
    except OSError: pass

    input_path = args.directory[0]
    file_list = os.listdir(input_path)
    output = open(output_path + 'banked_amr', 'w')
    for i in file_list:
        get_raw_amr.read_all(input_path, i, output)
    output.close()

    amr_table = amr_reader.main(open(output_path + 'banked_amr', 'r').read())
    if args.graph:
        amr_output.graph(amr_table)
    if args.node:
        amr_output.node(amr_table)
    if args.entity:
        amr_output.namedentity(amr_table)
    if args.path:
        import get_ne_query
        get_ne_query.main(amr_table)
        amr_output.path(amr_table)
    if args.query:
        import get_ne_query
        get_ne_query.main(amr_table)
        for docid in sorted(amr_table):
            for senid in sorted(amr_table[docid]):
                print senid
                sen = amr_table[docid][senid]

        #         for i in sen.amr_paths_:
        #             if i == 'rte':
        #                 for j in sen.amr_paths_[i]:
        #                     print j
        #         print

                # for ne in sen.named_entities_:
                #     print sen.named_entities_[ne].entity_name_
                #     print sen.named_entities_[ne].coherence_
                # print

        #         for i in sen.amr_paths_:
        #             print i
        #             for j in sen.amr_paths_[i]:
        #                 for k in j:
        #                     print k[0], k[1],
        #                 print

    if args.visualization:
        m = re.search('\/(\w+)\/', input_path[::-1])
        amr_output.html(amr_table, m.group(1)[::-1])
