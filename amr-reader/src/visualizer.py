'''
 AMR visualizer
 Please install
  - graphviz
  - pygraphviz

 Input: 'Sentence' object
 Output: AMR graphs
'''

import re
import pygraphviz as pgv

def visualizer(sen, output_path, show_wiki=True):
    nodes = set()
    for i in sen.graph_:
        nodes.add(i[0])
        nodes.add(i[1])

    ### Draw nodes
    G = pgv.AGraph(strict=False, directed=True)
    for i in nodes:
        if i == '@': # Root of AMR graph
            continue
        node = sen.amr_nodes_[i]
        pol = ''
        if node.polarity_:
            pol = '\npolarity'
        if node.ful_name_ != '':
            ### Node is a named entity
            if node.is_entity_:
                ne = sen.named_entities_[node.name_]
                if show_wiki:
                    ne_name = '%s\nwiki: %s' % (ne.entity_name_, ne.wiki_)
                else:
                    ne_name = '%s\n' % ne.entity_name_
                G.add_node(i, shape='point', fillcolor='red')
                G.add_node(i + '#' + ne.subtype_, shape='box', color='blue',
                           label=ne_name)
                G.add_edge(i, i + '#' + ne.subtype_,
                           label=ne.subtype_ + pol)
            ### Node is a instance
            else:
                full_name = '%s' % node.ful_name_
                G.add_node(i, shape='point', fillcolor='red')
                if re.match('\S+-\d+', full_name): # Node has sense tag
                    G.add_node(i + '#instance', shape='egg', color='orange',
                               label=full_name)
                else:
                    G.add_node(i + '#instance', shape='egg', color='green',
                               label=full_name)
                G.add_edge(i, i + '#instance', label='instance' + pol,
                           fontname='times italic')
        ### Node is only a concept
        else:
            G.add_node(i, shape='ellipse', color='black')

    ### Draw edge label
    for i in sen.graph_:
        if i[0] == '@':
            continue
        G.add_edge(i[0], i[1], label=i[2], fontname='monospace')

    G.layout()
    G.layout(prog='dot')
    G.draw('%s%s.png' % (output_path, sen.senid_))

def visualizer_curt(sen, output_path, show_wiki=True):
    nodes = set()
    for i in sen.graph_:
        nodes.add(i[0])
        nodes.add(i[1])

    ### Draw nodes
    G = pgv.AGraph(strict=False, directed=True)
    for i in nodes:
        if i == '@': # Root of AMR graph
            continue
        node = sen.amr_nodes_[i]
        pol = ''
        if node.polarity_:
            pol = '\n- polarity'
        if node.ful_name_ != '':
            ### Node is a named entity
            if node.is_entity_:
                if show_wiki:
                    ne_name = '%s\nwiki: %s' % (node.entity_name_, node.wiki_)
                else:
                    ne_name = '%s\n' % node.entity_name_
                G.add_node(i, shape='box', color='blue',
                           label=node.ful_name_ + '\n' + ne_name + pol)
            ### Node is a instance
            else:
                full_name = '%s' % node.ful_name_
                if re.match('\S+-\d+', full_name): # Node has sense tag
                    G.add_node(i, shape='egg', color='orange',
                               label=full_name + pol)
                else:
                    G.add_node(i, shape='egg', color='green',
                               label=full_name + pol)
        ### Node is only a concept
        else:
            G.add_node(i, shape='ellipse', color='black')

    ### Draw edge label
    for i in sen.graph_:
        if i[0] == '@':
            continue
        G.add_edge(i[0], i[1], label=i[2], fontname='monospace')

    G.layout()
    G.layout(prog='dot')
    G.draw('%s%s.png' % (output_path, sen.senid_))
