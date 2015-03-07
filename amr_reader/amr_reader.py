import re
import os
import sys
sys.setrecursionlimit(10000)
import copy
from node import Node
from amr_visualizer import visualizer
from get_html_output import html

'''
 input validator
'''
def amr_validator(raw_amr_input):
    if raw_amr_input.count('(') == 0:
        return False
    if raw_amr_input.count(')') == 0:
        return False
    if raw_amr_input.count('(') != raw_amr_input.count(')'):
        return False
    return True

'''
 input: raw amr
 output: amr_contents (list, golbal variable)
 functionality: split raw amr by pairing '()'
'''
def split_amr(text, content):
    # global amr_contents
    if len(text) == 0:
        return
    else:
        if text[0] == '(':
            content.append([])
            for i in content:
                i.append(text[0])
        elif text[0] == ')':
            for i in content:
                i.append(text[0])
            amr_contents.append(''.join(content[-1]))
            content.pop(-1)
        else:
            for i in content:
                i.append(text[0])
        text = text[1:]
        split_amr(text, content)

'''
 input: splited raw amr by pairing '()'
 output: node object (container: dict; 'amr_nodes' and 'amr_nodes_acr')
 single: only one pair of '()'
'''
def generate_node_single(content, amr_nodes, amr_nodes_acr):
    assert content.count('(') == 1 and content.count(')') == 1
    predict_event = re.search('(\w+)\s/\s(\S+)', content)
    acr = predict_event.group(1) # acronym
    ful = predict_event.group(2).strip(')') # full name

    # in case of :polarity -
    is_polarity = False
    if re.search(":polarity\s-", content) != None: 
        is_polarity = True

    # node is a named entity
    names = re.findall(':op\d\s\"\S+\"', content)
    if len(names) > 0:
        entity_name = ''
        for i in names:
            entity_name += re.match(':op\d\s\"(\S+)\"', i).group(1) + ' '
        new_node = Node(name=acr, ful_name=ful, is_entity=True,
                        entity_name=entity_name.strip())
        amr_nodes[content] = new_node
        amr_nodes_acr[acr] = new_node

    else:
        new_node = Node(name=acr, ful_name=ful, is_polarity=is_polarity)
        amr_nodes[content] = new_node
        amr_nodes_acr[acr] = new_node

'''
 input: splited raw amr by pairing '()'
 output: node object (container: dict; 'amr_nodes' and 'amr_nodes_acr')
 multiple: multiple pairs of '()'
'''
def generate_nodes_multiple(content, amr_nodes, amr_nodes_acr):
    assert content.count('(') > 1 and content.count(')') > 1
    assert content.count('(') == content.count(')')
    content_key = content # key of dict 'amr_nodes'
    arg_nodes = list()
    is_named_entity = False
    is_polarity = False
    
    # remove existing nodes from content and link nodes
    # always check the longest node first, because it may contain other nodes
    for i in sorted(amr_nodes, key=len, reverse=True): 
        if i in content:
            e = content.find(i)
            s = content[:e].rfind(':')
            role = re.search(':\S+\s', content[s:e]).group() # role (edge label)
            content = content.replace(role+i, '', 1)
            amr_nodes[i].edge_label_ = role.strip()
            if ':name' in role:
                is_named_entity = True
                ne = amr_nodes[i]
            else:
                arg_nodes.append(amr_nodes[i])

    predict_event = re.search('\w+\s/\s\S+', content).group().split(' / ')
    acr = predict_event[0] # acronym
    ful = predict_event[1] # full name

    # in case of :polarity -
    if re.search(":polarity\s-", content) != None: 
        is_polarity = True

    nodes = re.findall(':\S+\s\S+', content)
    for i in nodes:
        i = re.search('(:\S+)\s(\S+)', i)
        role = i.group(1)
        concept = i.group(2).strip(')')
        if role == ':wiki' and is_named_entity:
            continue
        if role == ':polarity':
            continue
        if concept in amr_nodes_acr:
            node = copy.copy(amr_nodes_acr[concept])
            node.next_ = list()
        else: # in case of (d / date-entity :year 2012)
            node = Node(name=concept)
            amr_nodes_acr[concept] = node
        node.edge_label_ = role
        arg_nodes.append(node)
        
    ''' named entity is a special node, thus, all concepts of a 
        named entity will be merged. For example, 
        (p / person :wiki -
           :name (n / name 
                    :op1 "Pascale"))
        will be consider as one node.

        According to AMR Specification, "we fill the :instance 
        slot from a special list of standard AMR named entity types". 
        Thus, for named entity node, we will use entity type 
        (p / person in the example) instead of :instance
    '''
    if is_named_entity:
        # find wikipedia title
        wikititle = 'None'
        # if re.match('\S+\s/\s\S+\s.*:wiki\s-', content) != None: wikititle = '-'
        if re.match(':wiki\s-', content) != None: wikititle = '-'
        else:
            m = re.search(':wiki\s\"(.+?)\"', content)
            if m != None: wikititle = m.group(1)
            else: wikititle = 'None'

        new_node = Node(name=acr, ful_name=ful, next_node=arg_nodes,
                        edge_label=ne.ful_name_, is_entity=True,
                        entity_type=ful, entity_name=ne.entity_name_,
                        wiki=wikititle, is_polarity=is_polarity)
        amr_nodes[content_key] = new_node
        amr_nodes_acr[acr] = new_node

    elif len(arg_nodes) > 0:
        new_node = Node(name=acr, ful_name=ful, next_node=arg_nodes,
                        is_polarity=is_polarity)
        amr_nodes[content_key] = new_node
        amr_nodes_acr[acr] = new_node

'''
 in case of single pair of '()' contains multiple nodes
 e.x. (m / moment :poss p5)
'''
def revise_node(content, amr_nodes, amr_nodes_acr):
    m = re.search('\w+\s/\s\S+\s+(.+)', content.replace('\n', ''))
    if m != None and \
       ' / name' not in content and \
       ':polarity -' not in content:
        arg_nodes = list()
        acr = re.search('\w+\s/\s\S+', content).group().split(' / ')[0]
        # nodes = re.findall('\S+\s\S+', m.group(1))
        nodes = re.findall('\S+\s\".+\"|\S+\s\S+', m.group(1)) # in case of :ARG2 "Tsai et al., 2002"
        for i in nodes:
            i = re.search('(:\S+)\s(.+)', i)
            role = i.group(1)
            concept = i.group(2).strip(')')
            if concept in amr_nodes_acr:
                node = copy.copy(amr_nodes_acr[concept])
                node.next_ = list()
            else: # in case of (d / date-entity :year 2012)
                node = Node(name=concept)
                amr_nodes_acr[concept] = node
            node.edge_label_ = role
            arg_nodes.append(node)
        amr_nodes_acr[acr].next_ = arg_nodes
        amr_nodes[content].next_ = arg_nodes
    
'''
 functionality: retrieve nodes and generate paths
'''
def retrieve_node(node, parent='@'):
    # global node_paths
    node_paths.append((parent, node.name_, node.edge_label_))
    for i in node.next_:
        retrieve_node(i, node.name_)
        
def amr_reader(raw_amr):
    global amr_contents
    amr_contents = list()
    global node_paths
    node_paths = list()
    amr_nodes = dict() # amr content as key
    amr_nodes_acr = dict() # acronym as key

    split_amr(raw_amr, list())
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            generate_node_single(i, amr_nodes, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') > 1 and i.count(')') > 1:
            generate_nodes_multiple(i, amr_nodes, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            revise_node(i, amr_nodes, amr_nodes_acr)

    # the last node (the whole raw amr) is always the root of the graph
    root = amr_nodes[sorted(amr_nodes, key=len, reverse=True)[0]]
    retrieve_node(root)

    return node_paths, amr_nodes, amr_nodes_acr

def main():
    try: os.mkdir('../output/graphs/')
    except OSError: pass

    input = open('../output/test', 'r').read()
    # input = open('../output/banked_amr', 'r').read()
    sentences = input.strip().split('# ::id ')
    sentences = sentences[1:]
    raw_amr = list()
    output = open('../output/test.html', 'w')
    # output = open('../output/banked_amr.html', 'w')
    output.write('<meta charset=\'utf-8\'>\n')
    for i in sentences:
        nline = i.split('\n')
        senid = nline[0]
        sen = nline[1]
        amr = '\n'.join(nline[2:]).strip()
        raw_amr.append((senid, sen, amr))
        print senid
        node_paths, amr_nodes, amr_nodes_acr = amr_reader(amr)
        visualizer(amr_nodes_acr, node_paths, '../output/graphs/', senid)
        html(senid, sen, amr, output)


        
if __name__ == '__main__':
    main()
