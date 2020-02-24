import os


def html_get_ne(ne):
    name = '<b>%s</b> ---> <code>%s</code> <br>' % \
           (ne.entity_name, ne.wiki)
    coreference = '&nbsp;<i>Coref. name: </i><code>%s</code><br>' % \
                  ne.coreference
    neighbors = '&nbsp;<i>Neighbors:&nbsp;&nbsp;&nbsp; </i> <code>'
    for i in ne.neighbors:
        neighbors += '%s ' % str(i)
    neighbors += '</code><br>'
    coherence = '&nbsp;<i>Coheret set:&nbsp </i> <code>'
    for i in ne.coherence:
        coherence += '(%s, %s, %s) ' % (i[0], i[1], i[2].entity_name)
    coherence += '</code><br>'
    return '%s\n%s\n%s\n%s\n<br>' % (name, coreference, neighbors, coherence)


def html_get_sentence(sent):
    graph = '<img src="./graphs/%s.png">' % sent.sentid
    senid = '<h2>%s</h2>' % sent.sentid
    comments = '<p><b>%s</b></p>' % sent.comments.split('\n')[0]
    sentence = '<p><b>%s</b></p>' % sent.sent
    amr = '<p><code>%s</code></p>' % sent.raw_amr \
          .replace('\n', '<br>') \
          .replace(' ', '&nbsp;')
    nes = '<button type="button" onclick="toggle_visibility(\'%s\');"><b>' \
          'Named Entities</b></button> &#9660;<br><div id="%s" ' \
          'style="display: none;">\n' % (sent.sentid, sent.sentid)
    for i in sent.named_entities:
        nes += html_get_ne(sent.named_entities[i])
    nes += '</div>'
    return '<body>\n%s\n%s\n%s\n%s\n%s\n%s\n</body>\n' % \
        (senid, sentence, amr, comments, nes, graph)


def get_html(sents, filename, outdir, curt=False):
    from src import visualizer
    with open('%s/%s.html' % (outdir, filename), 'w') as fw:
        graph_dir = '%s/%s' % (outdir, 'graphs')
        os.makedirs(graph_dir, exist_ok=True)
        phead = os.path.dirname(os.path.abspath(__file__)) + '/../static/html_head'
        fw.write(open(phead, 'r').read())

        for snt in sents:
            if curt:
                visualizer.visualizer_curt(snt, graph_dir)
            else:
                visualizer.visualizer(snt, graph_dir)
            fw.write(html_get_sentence(snt))


def get_graph(sents, outdir, curt=False):
    from src import visualizer
    graph_dir = '%s/%s' % (outdir, 'graphs')
    os.makedirs(graph_dir, exist_ok=True)
    for snt in sents:
        if curt:
            visualizer.visualizer_curt(snt, graph_dir)
        else:
            visualizer.visualizer(snt, graph_dir)


def get_node(sents, outdir):
    with open('%s/amr_nodes' % outdir, 'w') as fw:
        for snt in sents:
            for acr in sorted(snt.amr_nodes):
                node = snt.amr_nodes[acr]
                if node.ful_name == 'name': # Ingore 'n / name' node
                    pass
                else:
                    fw.write('%s\n%s\n' % (snt.sentid, node))


def get_namedentity(sents, outdir):
    with open('%s/amr_nes' % outdir, 'w') as fw:
        for snt in sents:
            for acr in sorted(snt.amr_nodes):
                node = snt.amr_nodes[acr]
                if node.is_entity:
                    fw.write('%s\t%s / %s\t%s\t%s\n' % \
                              (snt.sentid, node.name, node.ful_name,
                               node.entity_name, node.wiki))


def get_path(sents, outdir):
    with open('%s/amr_paths' % outdir, 'w') as fw:
        for snt in sents:
            for path_type in snt.amr_paths:
                paths = snt.amr_paths[path_type]
                for p in paths:
                    path = ''
                    for i in p:
                        path += '(\'%s\', \'%s\'), ' % (i[0], i[1])
                    fw.write('%s\t%s\t[%s]\n' % \
                             (snt.sentid, path_type, path.strip(', ')))


def get_query(sents, outdir):
    with open('%s/amr_queries' % outdir, 'w') as fw:
        for snt in sents:
            for i in snt.named_entities:
                ne = snt.named_entities[i]
                query = '%s(%s|%s)' % (ne.name(), ne.subtype, ne.maintype)
                for i in ne.neighbors:
                    query += '%s;' % i[1]
                query += '|'
                for i in ne.coherence:
                    query += '%s;' % i[2].name()
                fw.write('%s\t%s\t%s\n' % \
                         (snt.senid, ne.entity_name, query.strip(';')))


def get_newiki(amr_corpus, outdir):
    wiki = set()
    with open('%s/amr_nes_wiki' % outdir, 'w') as fw:
        for docid in sorted(amr_corpus):
            for sentid in sorted(amr_corpus[docid]):
                sent = amr_corpus[docid][sentid]
                assert sent.senid == sentid
                amr_nodes = sen.amr_nodes
                for n in amr_nodes:
                    node = amr_nodes[n]
                    if node.is_entity:
                        wiki.add(node.wiki)
        for i in sorted(wiki):
            fw.write('%s\n' % i)
