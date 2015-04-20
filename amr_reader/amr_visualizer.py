'''
 Please install graphviz and pygraphviz
'''

import re
import pygraphviz as pgv

'''
 Input: 'amr_nodes_acr': amr nodes table
        'path whole': path of whole graph
        'output_path': default output directory
        'output_name': default output name
        'show_wiki': display wikipedia title
 Output: amr graphs
'''
def visualizer(amr_nodes_acr, path_whole, output_path='../output/graphs/',
               output_name='amr_graph', show_wiki=True):
    nodes = set()
    for i in path_whole:
        nodes.add(i[0])
        nodes.add(i[1])

    # draw nodes
    G = pgv.AGraph(strict=False, directed=True)
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
    for i in path_whole:
        if i[0] == '@': continue
        G.add_edge(i[0], i[1], label=i[2], fontname='monospace')

    G.layout()
    G.layout(prog = 'dot')
    G.draw('%s%s.png' % (output_path, output_name))

def visualizer_easy(amr_nodes_acr, path_whole, output_path='../output/graphs/',
                    output_name='amr_graph', show_wiki=True):
    nodes = set()
    for i in path_whole:
        nodes.add(i[0])
        nodes.add(i[1])

    # draw nodes
    G = pgv.AGraph(strict=False, directed=True)
    for i in nodes:
        if i == '@': continue
        node = amr_nodes_acr[i]
        pol = ''
        if node.is_polarity_:
            pol = '\n- polarity'
        if node.ful_name_ != '':
            if node.is_entity_: # node is a named entity
                if show_wiki:
                    ne_name = '%s\nwiki: %s' % (node.entity_name_.decode("utf-8"), node.wiki_)
                else:
                    ne_name = '%s\n' % node.entity_name_.decode("utf-8")
                G.add_node(i, shape='box', color='blue', label=node.ful_name_+'\n'+ne_name+pol)
            else: # node is a instance
                full_name = '%s' % node.ful_name_
                if re.match('\S+-\d+', full_name): # node has sense tag
                    G.add_node(i, shape='egg', color='orange', label=full_name+pol)
                else:
                    G.add_node(i, shape='egg', color='green', label=full_name+pol)
        else: # node is only a concept
            G.add_node(i, shape='ellipse', color='black')

    # draw edge label
    for i in path_whole:
        if i[0] == '@': continue
        G.add_edge(i[0], i[1], label=i[2], fontname='monospace')

    G.layout()
    G.layout(prog = 'dot')
    G.draw('%s%s.png' % (output_path, output_name))
