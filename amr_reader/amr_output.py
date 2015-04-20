import os

'''
 html
'''
def get_path(name, paths):
    result = '<b>%s</b>\n<br>\n' % name
    p = ''
    for i in paths:
        for j in i:
            role = j[0]
            concept = j[1]
            if role == '@root' or role == '@entity':
                p += '<font face="arial">%s</font>' % concept
            else:
                p += ' --> <font face="verdana" color="orange">%s</font> <font face="arial">%s</font>' % (role, concept)
        p += '<br>'
    return result + p + '\n'

def get_html(senid, sen, amr, amr_paths, output):
    graph = '<img src="./graphs/%s.png">' % senid # default path of graphs: ./graphs/
    senid = '<h2>%s</h2>\n' % senid
    sen = '<p><b>%s</b></p>\n' % sen
    amr = '<p><code>%s</code></p>\n' % amr.replace('\n', '<br>').replace(' ', '&nbsp;')
    paths = ''
    # paths = '<p><b>Paths:</b><br>'
    # for p in amr_paths:
    #     paths += get_path(p, amr_paths[p])
    output.write('<body>\n%s%s%s%s%s</body>\n' % (senid, sen, amr, paths, graph))

def html(amr_table, filename='test', output_path='../output/', graph_path='../output/graphs/'):
    output = open(output_path + '%s.html' % filename, 'w')
    import amr_visualizer

    try: os.mkdir(graph_path)
    except OSError: pass

    output.write('<meta charset=\'utf-8\'>\n')

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_visualizer.visualizer(sen.amr_nodes_, sen.path_whole_, output_name=sen.senid_)
            get_html(sen.senid_, sen.sen_, sen.amr_, sen.amr_paths_, output)

'''
 AMR graphs
'''
def graph(amr_table, graph_path='../output/graphs/'):
    import amr_visualizer

    try: os.mkdir(graph_path)
    except OSError: pass

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_visualizer.visualizer(sen.amr_nodes_, sen.path_whole_, output_name=sen.senid_)

'''
 AMR nodes
 if you would like to modify the output format of AMR node, go to
 node.py: def __str__(self):
'''
def node(amr_table, output_path='../output/'):
    output = open(output_path + 'amr_nodes', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.is_entity_ and node.entity_type_ == '':
                    pass
                else:
                    output.write('%s\n%s\n' % (senid, amr_nodes[n])) 

'''
 named entities
'''
def namedentity(amr_table, output_path='../output/'):
    output = open(output_path + 'amr_nes', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.is_entity_ and node.entity_type_ != '':
                    output.write('%s\t%s / %s\t%s\t%s\n' % (senid,
                                                            node.name_,
                                                            node.ful_name_,
                                                            node.entity_name_,
                                                            node.wiki_))

'''
 AMR paths
'''
def path(amr_table, output_path='../output/'):
    output = open(output_path + 'amr_paths', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            for path_type in sen.amr_paths_:
                # if path_type != 'etl': continue
                paths = sen.amr_paths_[path_type]
                for p in paths:
                    path = ''
                    for i in p:
                        path += '(\'%s\', \'%s\'), ' % (i[0], i[1])
                    output.write('%s\t%s\t[%s]\n' % (senid,
                                                     path_type,
                                                     path.strip(', ')))
