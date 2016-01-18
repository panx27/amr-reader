'''
 AMR output functions
'''

import os

'''
 HTML
'''
def get_ne(ne):
    name = '<b>%s</b> ---> <code>%s</code> <br>' % (ne.entity_name_,
                                                         ne.wiki_)
    coreference = '&nbsp;<i>Coref. name: ' \
                  '</i><code>%s</code><br>' % ne.coreference_
    neighbors = '&nbsp;<i>Neighbors:&nbsp;&nbsp;&nbsp; </i> <code>'
    for i in ne.neighbors_:
        neighbors += '%s ' % str(i)
    neighbors += '</code><br>'
    coherence = '&nbsp;<i>Coheret set:&nbsp </i> <code>'
    for i in ne.coherence_:
        coherence += '(%s, %s, %s) ' % (i[0], i[1], i[2].entity_name_)
    coherence += '</code><br>'
    return '%s\n%s\n%s\n%s\n<br>' % (name, coreference, neighbors, coherence)

def get_sentence(sen, out):
    graph = '<img src="./graphs/%s.png">' % sen.senid_
    senid = '<h2>%s</h2>' % sen.senid_
    sentence = '<p><b>%s</b></p>' % sen.sen_
    amr = '<p><code>%s</code></p>' % sen.amr_. \
          replace('\n', '<br>'). \
          replace(' ', '&nbsp;')
    nes = '<button type="button" onclick="toggle_visibility(\'%s\');"><b>' \
          'Named Entities</b></button> &#9660;<br><div id="%s" ' \
          'style="display: none;">\n' % (sen.senid_, sen.senid_)
    for n in sen.named_entities_:
        nes += get_ne(sen.named_entities_[n])
    nes += '</div>'
    out.write('<body>\n%s\n%s\n%s\n%s\n%s\n</body>\n' % (senid, sentence,
                                                         amr, nes, graph))

def html(amres, filename, outdir, curt=False):
    out = open('%s/%s.html' % (outdir, filename), 'w')
    import visualizer

    graphdir = '%s/%s' % (outdir, 'graphs')
    try:
        os.mkdir(graphdir)
    except OSError:
        pass

    # head = '<meta charset=\'utf-8\'>\n'
    head = os.path.dirname(os.path.abspath(__file__)) + '/../docs/html_head'
    out.write(open(head, 'r').read())

    for snt in amres:
        if curt:
            visualizer.visualizer_curt(snt, graphdir)
        else:
            visualizer.visualizer(snt, graphdir)
        get_sentence(snt, out)

'''
 Visualized AMR graphs
 Input: 'Sentence' object
'''
def graph(amres, outdir, curt=False):
    import visualizer

    graphdir = '%s/%s' % (outdir, 'graphs')
    try:
        os.mkdir(graphdir)
    except OSError:
        pass

    for snt in amres:
        if curt:
            visualizer.visualizer_curt(snt, graphdir)
        else:
            visualizer.visualizer(snt, graphdir)

'''
 AMR nodes
  if you would like to modify the output format of AMR node, modify
  node.py: def __str__(self):
'''
def node(amres, outdir):
    out = open('%s/amr_nodes' % outdir, 'w')
    for snt in amres:
        for acr in snt.amr_nodes_:
            node = snt.amr_nodes_[acr]
            if node.ful_name_ == 'name': # Ingore 'n / name' node
                pass
            else:
                out.write('%s\n%s\n' % (snt.senid_, node))

'''
 Named entities
'''
def namedentity(amres, outdir):
    out = open('%s/amr_nes' % outdir, 'w')
    for snt in amres:
        for acr in snt.amr_nodes_:
            node = snt.amr_nodes_[acr]
            if node.is_entity_:
                out.write('%s\t%s / %s\t%s\t%s\n' % (snt.senid_, node.name_,
                                                     node.ful_name_,
                                                     node.entity_name_,
                                                     node.wiki_))

'''
 AMR paths
'''
def path(amres, outdir):
    out = open('%s/amr_paths' % outdir, 'w')
    for snt in amres:
        for path_type in snt.amr_paths_:
            paths = snt.amr_paths_[path_type]
            for p in paths:
                path = ''
                for i in p:
                    path += '(\'%s\', \'%s\'), ' % (i[0], i[1])
                out.write('%s\t%s\t[%s]\n' % (snt.senid_,
                                              path_type,
                                              path.strip(', ')))

'''
 AMR named entity queries
'''
def query(amres, outdir):
    out = open('%s/amr_queries' % outdir, 'w')
    for snt in amres:
        for i in snt.named_entities_:
            ne = snt.named_entities_[i]
            query = '%s(%s|%s)' % (ne.name(), ne.subtype_, ne.maintype_)
            for i in ne.neighbors_:
                query += '%s;' % i[1]
            query += '|'
            for i in ne.coherence_:
                query += '%s;' % i[2].name()

            out.write('%s\t%s\t%s\n' % (snt.senid_,
                                        ne.entity_name_,
                                        query.strip(';')))

'''
 Named entity wiki titile
'''
def newiki(amr_table, outdir):
    wiki = set()
    output = open(outdir + 'amr_nes_wiki', 'w')
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
