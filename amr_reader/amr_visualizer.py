import re
import pygraphviz as pgv



'''
 input: amr_nodes_acr, nodes_paths
 output: amr graph
'''
def visualizer(amr_nodes_acr, node_paths, output_path='', output_name='amr_graph', show_wiki=True):
    nodes = set()
    for i in node_paths:
        nodes.add(i[0])
        nodes.add(i[1])

    # draw nodes
    G = pgv.AGraph(strict=False, directed=True, encoding='UTF-8')
    for i in nodes:
        if i == '@': continue
        node = amr_nodes_acr[i]
        pol = ''
        if node.is_polarity_:
            pol = '\npolarity'
        if node.ful_name_ != '':
            if node.is_entity_: # node is a named entity
                if show_wiki:
                    ne_name = '%s\nwiki: %s' % (node.entity_name_.decode("utf-8"), node.wiki_)
                else:
                    ne_name = '%s\n' % node.entity_name_.decode("utf-8")
                G.add_node(i, shape='point', fillcolor='red')
                G.add_node(i+'#'+node.ful_name_, shape='box', color='blue', label=ne_name)
                G.add_edge(i, i+'#'+node.ful_name_, label=node.ful_name_+pol)
            else: # node is a instance
                full_name = '%s' % node.ful_name_
                G.add_node(i, shape='point', fillcolor='red')
                if re.match('\S+-\d+', full_name): # node has sense tag
                    G.add_node(i+'#instance', shape='egg', color='orange', label=full_name)
                else:
                    G.add_node(i+'#instance', shape='egg', color='green', label=full_name)
                G.add_edge(i, i+'#instance', label='instance'+pol, fontname='times italic')
        else: # node is only a concept
            G.add_node(i, shape='ellipse', color='black')

    # draw edge label
    for i in node_paths:
        if i[0] == '@': continue
        G.add_edge(i[0], i[1], label=i[2], fontname='monospace')

    G.layout()
    G.layout(prog = 'dot')
    G.draw('%s%s.png' % (output_path, output_name))
    # G.draw('%s%s.pdf' % (output_path, output_name))
