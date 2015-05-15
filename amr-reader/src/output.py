'''
 AMR output functions
'''

import os

'''
 HTML format
'''
def get_ne(ne):
    name = '<b><i>%s</i></b>\n<br>\n' % ne.entity_name_
    coreference = '&nbsp;&nbsp;<i>Coreferential name: ' \
                  '</i><font face="arial">%s</font><br>' % ne.coreference_
    neighbors = '&nbsp;&nbsp;<i>Neighbors: </i> <font face="arial">'
    for i in ne.neighbors_:
        neighbors += '%s ' % str(i)
    neighbors += '</font><br>'
    coherence = '&nbsp;&nbsp;<i>Coheret set: </i> <font face="arial">'
    for i in ne.coherence_:
        coherence += '(\'%s\', \'%s\', \'%s\') ' % (i[0], i[1], i[2].entity_name_)
    coherence += '</font><br>'
    return name + coreference + neighbors + coherence + '\n'

def get_sentence(sen, output):
    graph = '<img src="./graphs/%s.png">' % sen.senid_
    senid = '<h2>%s</h2>\n' % sen.senid_
    sentence = '<p><b>%s</b></p>\n' % sen.sen_
    amr = '<p><code>%s</code></p>\n' % sen.amr_. \
          replace('\n', '<br>'). \
          replace(' ', '&nbsp;')
    nes = '<p>Named Entities:<br>'
    for n in sen.named_entities_:
        nes += get_ne(sen.named_entities_[n])
    output.write('<body>\n%s%s%s%s%s</body>\n' % (senid, sentence,
                                                  amr, nes, graph))

def html(amr_table, filename, output_path):
    output = open(output_path + '%s.html' % filename, 'w')
    import visualizer

    graph_path = output_path + 'graphs/'
    try: os.mkdir(graph_path)
    except OSError: pass

    output.write('<meta charset=\'utf-8\'>\n')

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            visualizer.visualizer(sen, graph_path)
            get_sentence(sen, output)

'''
 AMR graphs
  Input: 'Sentence' object
'''
def graph(amr_table, output_path, curt=False):
    import visualizer

    graph_path = output_path + 'graphs/'
    try: os.mkdir(graph_path)
    except OSError: pass

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            if curt:
                visualizer.visualizer_curt(sen, graph_path)
            else:
                visualizer.visualizer(sen, graph_path)

'''
 AMR nodes
  if you would like to modify the output format of AMR node, modify
  node.py: def __str__(self):
'''
def node(amr_table, output_path):
    output = open(output_path + 'amr_nodes', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.ful_name_ == 'name': # Ingore 'n / name' node
                    pass
                else:
                    output.write('%s\n%s\n' % (senid, node))

'''
 Named entities
'''
def namedentity(amr_table, output_path):
    output = open(output_path + 'amr_nes', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.is_entity_:
                    output.write('%s\t%s / %s\t%s\t%s\n' % (senid, node.name_,
                                                            node.ful_name_,
                                                            node.entity_name_,
                                                            node.wiki_))

'''
 AMR paths
'''
def path(amr_table, output_path):
    output = open(output_path + 'amr_paths', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            for path_type in sen.amr_paths_:
                paths = sen.amr_paths_[path_type]
                for p in paths:
                    path = ''
                    for i in p:
                        path += '(\'%s\', \'%s\'), ' % (i[0], i[1])
                    output.write('%s\t%s\t[%s]\n' % (senid,
                                                     path_type,
                                                     path.strip(', ')))

'''
 AMR named entity queries
'''
def query(amr_table, output_path):
    output = open(output_path + 'amr_queries', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            for i in sen.named_entities_:
                ne = sen.named_entities_[i]
                query = '%s(%s|%s)' % (ne.name(), ne.subtype_, ne.maintype_)
                for i in ne.neighbors_:
                    query += '%s;' % i[1]
                query += '|'
                for i in ne.coherence_:
                    query += '%s;' % i[2].name()

                output.write('%s\t%s\t%s\n' % (senid,
                                               ne.entity_name_,
                                               query.strip(';')))

'''
 Named entity wiki titile
'''
def newiki(amr_table, output_path):
    wiki = set()
    output = open(output_path + 'amr_nes_wiki', 'w')
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            assert sen.senid_ == senid
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.is_entity_:
                    wiki.add(node.wiki_)
    for i in sorted(wiki):
        output.write('%s\n' % i)
