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
 retrieve path - whole graph
'''
def retrieve_path_whole(node, parent, paths_whole):
    paths_whole.append((parent, node.name_, node.edge_label_))
    for i in node.next_:
        retrieve_path_whole(i, node.name_, paths_whole)

'''
 retrieve path - root to entity
'''
def retrieve_path_rte(node, path, paths_rte):
    for i in node.next_:
        tmp = path[:] # passing by value
        if i.is_entity_:
            ne = '%s\t%s' % (i.entity_type_, i.entity_name_)
            path.append((i.edge_label_, ne))
            paths_rte.append(path)
            path = tmp
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_rte(i, tmp, paths_rte)

'''
 retrieve path - entity to leaf
'''
def retrieve_path_etl(node, path, paths_etl):
    if node.next_ == list():
        paths_etl.append(path)
    for i in node.next_:
        tmp = path[:] # passing by value
        if i.is_entity_:
            ne = '%s\t%s' % (i.entity_type_, i.entity_name_)
            tmp.append((i.edge_label_, ne))
            retrieve_path_rte(i, tmp, paths_rte)
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_etl(i, tmp, paths_etl)

'''
 amr reader
'''
def amr_reader(raw_amr_input):
    global amr_contents
    amr_contents = list()
    amr_nodes = dict() # amr content as key
    amr_nodes_acr = dict() # acronym as key
    paths_whole = list()
    paths_rte = list()
    paths_etl = list()
    
    split_amr(raw_amr_input, list())
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            generate_node_single(i, amr_nodes, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') > 1 and i.count(')') > 1:
            generate_nodes_multiple(i, amr_nodes, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            revise_node(i, amr_nodes, amr_nodes_acr)

    # the last node (whole amr) is always the root of the graph
    root = amr_nodes[sorted(amr_nodes, key=len, reverse=True)[0]]
    retrieve_path_whole(root, '@', paths_whole)

    retrieve_path_rte(root, [('@root', root.ful_name_)], paths_rte)
    # for i in paths_rte: print i

    for i in amr_nodes_acr:
        node = amr_nodes_acr[i]
        if node.is_entity_ and node.next_ != list():
            ne = ('@entity', node.entity_type_+'\t'+node.entity_name_)
            retrieve_path_etl(node, [ne], paths_etl)
    # for i in paths_etl: print i

    return amr_nodes, amr_nodes_acr, paths_whole, paths_rte, paths_etl

'''
 main function
 input: raw amr
 output: amr graph
         amr path
'''
def main(input, output, graph_path='../output/graphs/'):
    sentences = input.strip().split('# ::id ')
    sentences = sentences[1:]
    raw_amr = list()

    for i in sentences:
        nline = i.split('\n')
        senid = nline[0]
        sen = nline[1]
        amr = '\n'.join(nline[2:]).strip()
        raw_amr.append((senid, sen, amr))
        print senid
        if amr_validator(amr) == False:
            raise NameError('Invalid AMR Input: %s' % sen_id)
        amr_nodes, amr_nodes_acr, paths_whole, paths_rte, paths_etl = amr_reader(amr)

        visualizer(amr_nodes_acr, paths_whole, graph_path, senid)
        html(senid, sen, amr, paths_rte, paths_etl, output)

if __name__ == '__main__':
    graph_path = '../output/graphs/'
    try: os.mkdir(graph_path)
    except OSError: pass

    input = open('../output/test', 'r').read()
    # input = open('../output/banked_amr', 'r').read()

    output = open('../output/test.html', 'w')
    # output = open('../output/banked_amr.html', 'w')
    output.write('<meta charset=\'utf-8\'>\n')

    main(input, output, graph_path)
