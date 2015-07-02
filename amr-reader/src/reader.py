'''
 AMR reader
'''

import re
import os
import sys
sys.setrecursionlimit(10000)
import copy
from Node import Node
from Sentence import Sentence

'''
 Input validator
'''
def amr_validator(raw_amr_input): # TODO: add more test cases
    if raw_amr_input.count('(') == 0:
        return False
    if raw_amr_input.count(')') == 0:
        return False
    if raw_amr_input.count('(') != raw_amr_input.count(')'):
        return False
    return True

'''
 Input: raw AMR
 Output: amr_contents (list(), golbal variable)
 Functionality: split raw amr by pairing '()'
'''
def split_amr(text, content):
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
 Input: splited AMR: single pair of '()'
 Output: generate Node object
         containers: 'amr_nodes_con' - amr content as key
                     'amr_nodes_acr' - acronym as key
'''
def generate_node_single(content, amr_nodes_con, amr_nodes_acr):
    assert content.count('(') == 1 and content.count(')') == 1
    predict_event = re.search('(\w+)\s/\s(\S+)', content)
    acr = predict_event.group(1) # Acronym
    ful = predict_event.group(2).strip(')') # Full name

    ### In case of :polarity -
    is_polarity = False
    if re.search(":polarity\s-", content) != None:
        is_polarity = True

    ### Node is a named entity
    names = re.findall(':op\d\s\"\S+\"', content)
    if len(names) > 0:
        entity_name = ''
        for i in names:
            entity_name += re.match(':op\d\s\"(\S+)\"', i).group(1) + ' '
        new_node = Node(name=acr, ful_name=ful,
                        entity_name=entity_name.strip(), polarity=is_polarity)
        amr_nodes_con[content] = new_node
        amr_nodes_acr[acr] = new_node
    else:
        new_node = Node(name=acr, ful_name=ful, polarity=is_polarity)
        amr_nodes_con[content] = new_node
        amr_nodes_acr[acr] = new_node

'''
 Input: splited AMR: multiple pairs of '()'
 Output: generate Node object
         containers: 'amr_nodes_con' - amr content as key
                     'amr_nodes_acr' - acronym as key
'''
def generate_nodes_multiple(content, amr_nodes_con, amr_nodes_acr):
    assert content.count('(') > 1 and content.count(')') > 1
    assert content.count('(') == content.count(')')
    content_key = content # Key of dict() 'amr_nodes_con'
    arg_nodes = list()
    is_named_entity = False
    is_polarity = False

    '''
     remove existing nodes from the content, and link those
     nodes to the root of subtree
    '''
    for i in sorted(amr_nodes_con, key=len, reverse=True):
        if i in content:
            e = content.find(i)
            s = content[:e].rfind(':')
            role = re.search(':\S+\s', content[s:e]).group() # Edge label
            content = content.replace(role+i, '', 1)
            amr_nodes_con[i].edge_label_ = role.strip()
            if ':name' in role:
                is_named_entity = True
                ne = amr_nodes_con[i]
            else:
                arg_nodes.append(amr_nodes_con[i])

    predict_event = re.search('\w+\s/\s\S+', content).group().split(' / ')
    acr = predict_event[0] # Acronym
    ful = predict_event[1] # Full name

    ### In case of :polarity -
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
        else: # In case of (d / date-entity :year 2012)
            node = Node(name=concept)
            amr_nodes_acr[concept] = node
        node.edge_label_ = role
        arg_nodes.append(node)

    '''
        Named entity is a special node, so the subtree of a
        named entity will be merged. For example,
        (p / person :wiki -
           :name (n / name
                    :op1 "Pascale"))
        will be consider as one node.

        According to AMR Specification, "we fill the :instance
        slot from a special list of standard AMR named entity types".
        Thus, for named entity node, we will use entity type
        (p / person in the example above) instead of :instance
    '''
    if is_named_entity:
        ### Find Wikipedia title:
        wikititle = ''
        if re.match('.+:wiki\s-.*', content) != None:
            wikititle = '-' # Entity is NIL, Wiki title does not exist
        else:
            m = re.search(':wiki\s\"(.+?)\"', content)
            if m != None:
                wikititle = m.group(1) # Wiki title
            else:
                wikititle = '' # There is no Wiki title information

        new_node = Node(name=acr, ful_name=ful, next_node=arg_nodes,
                        edge_label=ne.ful_name_, is_entity=True,
                        entity_type=ful, entity_name=ne.entity_name_,
                        wiki=wikititle, polarity=is_polarity)
        amr_nodes_con[content_key] = new_node
        amr_nodes_acr[acr] = new_node

    elif len(arg_nodes) > 0:
        new_node = Node(name=acr, ful_name=ful, next_node=arg_nodes,
                        polarity=is_polarity)
        amr_nodes_con[content_key] = new_node
        amr_nodes_acr[acr] = new_node

'''
 In case of single pair of '()' contains multiple nodes
 e.x. (m / moment :poss p5)
'''
def revise_node(content, amr_nodes_con, amr_nodes_acr):
    m = re.search('\w+\s/\s\S+\s+(.+)', content.replace('\n', ''))
    if m != None and \
       ' / name' not in content and \
       ':polarity -' not in content:
        arg_nodes = list()
        acr = re.search('\w+\s/\s\S+', content).group().split(' / ')[0]
        nodes = re.findall('\S+\s\".+\"|\S+\s\S+', m.group(1))
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
        amr_nodes_con[content].next_ = arg_nodes

'''
 Retrieve path - whole graph
'''
def retrieve_graph(node, parent, graph):
    graph.append((parent, node.name_, node.edge_label_))
    for i in node.next_:
        retrieve_graph(i, node.name_, graph)

'''
 AMR reader
'''
def amr_reader(raw_amr_input):
    global amr_contents
    amr_contents = list()
    amr_nodes_con = dict() # AMR content as key
    amr_nodes_acr = dict() # Acronym as key
    graph = list() # Path of whole graph

    split_amr(raw_amr_input, list())
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            generate_node_single(i, amr_nodes_con, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') > 1 and i.count(')') > 1:
            generate_nodes_multiple(i, amr_nodes_con, amr_nodes_acr)
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            revise_node(i, amr_nodes_con, amr_nodes_acr)

    # The longest node (whole AMR) is always the root of the AMR graph
    root = amr_nodes_con[sorted(amr_nodes_con, key=len, reverse=True)[0]]
    retrieve_graph(root, '@', graph)

    return amr_nodes_acr, graph

'''
 Main function

 Input: raw AMR
 Output: 'amr_table'
         container: dict()   dict()      Sentence
         key:       docid -> senid -> sentence object
'''
def main(input_):
    amr_table = dict()
    sentences = input_.strip().split('# ::id ')

    for i in sentences:
        if i == '': continue
        nline = i.split('\n')
        senid = re.search('(\S+)', nline[0]).group(1)
        docid = senid[:senid.rfind('.')]
        sen = re.search('# ::snt (.+)', nline[1]).group(1)
        # if nline[2].startswith('# ::save-date'): # ingore save-date info
        #     nline.remove(nline[2])
        amr = '\n'.join(nline[2:]).strip()

        if amr_validator(amr) == False:
            raise NameError('Invalid AMR Input: %s' % senid)

        amr_nodes_acr, graph = amr_reader(amr)

        if docid not in amr_table:
            amr_table[docid] = dict()
        amr_table[docid][senid] = Sentence(senid, sen, amr,
                                           amr_nodes_acr, graph)
    return amr_table
