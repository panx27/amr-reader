import sys
sys.setrecursionlimit(10000)
import os
import re
import copy
import urllib.parse
import uuid

from .models.Node import Node
from .models.Sentence import Sentence


def amr_validator(raw_amr): # TODO: add more test cases
    '''
    AMR validator

    :param str raw_amr:
    :return bool:
    '''
    if raw_amr.count('(') == 0:
        return False
    if raw_amr.count(')') == 0:
        return False
    if raw_amr.count('(') != raw_amr.count(')'):
        return False
    return True


def split_amr(raw_amr, contents):
    '''
    Split raw AMR based on '()'

    :param str raw_amr:
    :param list contentss:
    '''
    if not raw_amr:
        return
    else:
        if raw_amr[0] == '(':
            contents.append([])
            for i in contents:
                i.append(raw_amr[0])
        elif raw_amr[0] == ')':
            for i in contents:
                i.append(raw_amr[0])
            amr_contents.append(''.join(contents[-1]))
            contents.pop(-1)
        else:
            for i in contents:
                i.append(raw_amr[0])
        raw_amr = raw_amr[1:]
        split_amr(raw_amr, contents)


def generate_node_single(content, amr_nodes_content, amr_nodes_acronym):
    '''
    Generate Node object for single '()'

    :param str context:
    :param dict amr_nodes_content: content as key
    :param dict amr_nodes_acronym: acronym as key
    '''
    try:
        assert content.count('(') == 1 and content.count(')') == 1
    except AssertionError:
        raise Exception('Unmatched parenthesis')

    predict_event = re.search('(\w+)\s/\s(\S+)', content)
    if predict_event:
        acr = predict_event.group(1) # Acronym
        ful = predict_event.group(2).strip(')') # Full name
    else:
        acr, ful = '-', '-'

    # In case of :polarity -
    is_polarity = True if re.search(":polarity\s-", content) else False

    # :ARG ndoes
    arg_nodes = []
    nodes = re.findall(':\S+\s\S+', content)
    for i in nodes:
        i = re.search('(:\S+)\s(\S+)', i)
        role = i.group(1)
        concept = i.group(2).strip(')')
        if role == ':wiki':
            continue
        if role == ':polarity':
            continue
        if concept in amr_nodes_acronym:
            node = copy.copy(amr_nodes_acronym[concept])
            node.next_nodes = []
        # In case of (d / date-entity :year 2012)
        else:
            node = Node(name=concept)
            amr_nodes_acronym[concept] = node
        node.edge_label = role
        arg_nodes.append(node)

    # Node is a named entity
    names = re.findall(':op\d\s\"\S+\"', content)
    if len(names) > 0:
        entity_name = ''
        for i in names:
            entity_name += re.match(':op\d\s\"(\S+)\"', i).group(1) + ' '
        entity_name = urllib.parse.unquote_plus(entity_name.strip())
        new_node = Node(name=acr, ful_name=ful, next_nodes=arg_nodes,
                        entity_name=entity_name,
                        polarity=is_polarity, content=content)
        amr_nodes_content[content] = new_node
        amr_nodes_acronym[acr] = new_node
    else:
        new_node = Node(name=acr, ful_name=ful, next_nodes=arg_nodes,
                        polarity=is_polarity, content=content)
        amr_nodes_content[content] = new_node
        amr_nodes_acronym[acr] = new_node


def generate_nodes_multiple(content, amr_nodes_content, amr_nodes_acronym):
    '''
    Generate Node object for nested '()'

    :param str context:
    :param dict amr_nodes_content: content as key
    :param dict amr_nodes_acronym: acronym as key
    '''
    try:
        assert content.count('(') > 1 and content.count(')') > 1
        assert content.count('(') == content.count(')')
    except AssertionError:
        raise Exception('Unmatched parenthesis')

    _content = content
    arg_nodes = []
    is_named_entity = False

    # Remove existing nodes from the content, and link these nodes to the root
    # of the subtree
    for i in sorted(amr_nodes_content, key=len, reverse=True):
        if i in content:
            e = content.find(i)
            s = content[:e].rfind(':')
            role = re.search(':\S+\s', content[s:e]).group() # Edge label
            content = content.replace(role+i, '', 1)
            amr_nodes_content[i].edge_label = role.strip()
            if ':name' in role:
                is_named_entity = True
                ne = amr_nodes_content[i]
            else:
                arg_nodes.append(amr_nodes_content[i])

    predict_event = re.search('\w+\s/\s\S+', content).group().split(' / ')
    if predict_event:
        acr = predict_event[0] # Acronym
        ful = predict_event[1] # Full name
    else:
        acr, ful = '-', '-'

    # In case of :polarity -
    is_polarity = True if re.search(":polarity\s-", content) else False

    nodes = re.findall(':\S+\s\S+', content)
    for i in nodes:
        i = re.search('(:\S+)\s(\S+)', i)
        role = i.group(1)
        concept = i.group(2).strip(')')
        if role == ':wiki' and is_named_entity:
            continue
        if role == ':polarity':
            continue
        if concept in amr_nodes_acronym:
            node = copy.copy(amr_nodes_acronym[concept])
            node.next_nodes = []
        # In case of (d / date-entity :year 2012)
        else:
            node = Node(name=concept)
            amr_nodes_acronym[concept] = node
        node.edge_label = role
        arg_nodes.append(node)

        # Named entity is a special node, so the subtree of a
        # named entity will be merged. For example,
        #     (p / person :wiki -
        #        :name (n / name
        #                 :op1 "Pascale"))
        # will be merged as one node.
        # According to AMR Specification, "we fill the :instance
        # slot from a special list of standard AMR named entity types".
        # Thus, for named entity node, we will use entity type
        # (p / person in the example above) instead of :instance

    if is_named_entity:
        # Get Wikipedia title:
        if re.match('.+:wiki\s-.*', content):
            wikititle = '-' # Entity is NIL, Wiki title does not exist
        else:
            m = re.search(':wiki\s\"(.+?)\"', content)
            if m:
                wikititle = urllib.parse.unquote_plus(m.group(1)) # Wiki title
            else:
                wikititle = '' # There is no Wiki title information

        new_node = Node(name=acr, ful_name=ful, next_nodes=arg_nodes,
                        edge_label=ne.ful_name, is_entity=True,
                        entity_type=ful, entity_name=ne.entity_name,
                        wiki=wikititle, polarity=is_polarity, content=content)
        amr_nodes_content[_content] = new_node
        amr_nodes_acronym[acr] = new_node

    elif len(arg_nodes) > 0:
        new_node = Node(name=acr, ful_name=ful, next_nodes=arg_nodes,
                        polarity=is_polarity, content=content)
        amr_nodes_content[_content] = new_node
        amr_nodes_acronym[acr] = new_node


def revise_node(content, amr_nodes_content, amr_nodes_acronym):
    '''
    In case of single '()' contains multiple nodes
    e.x. (m / moment :poss p5)

    :param str context:
    :param dict amr_nodes_content: content as key
    :param dict amr_nodes_acronym: acronym as key
    '''
    m = re.search('\w+\s/\s\S+\s+(.+)', content.replace('\n', ''))
    if m and ' / name' not in content and ':polarity -' not in content:
        arg_nodes = []
        acr = re.search('\w+\s/\s\S+', content).group().split(' / ')[0]
        nodes = re.findall('\S+\s\".+\"|\S+\s\S+', m.group(1))
        for i in nodes:
            i = re.search('(:\S+)\s(.+)', i)
            role = i.group(1)
            concept = i.group(2).strip(')')
            if concept in amr_nodes_acronym:
                node = copy.copy(amr_nodes_acronym[concept])
                node.next_nodes = []
            else: # in case of (d / date-entity :year 2012)
                node = Node(name=concept)
                amr_nodes_acronym[concept] = node
            node.edge_label = role
            arg_nodes.append(node)
        amr_nodes_acronym[acr].next_nodes = arg_nodes
        amr_nodes_content[content].next_nodes = arg_nodes


def retrieve_path(node, parent, path):
    '''
    Retrieve AMR nodes path

    :param Node_object node:
    :param str parent:
    :param list path:
    '''
    path.append((parent, node.name, node.edge_label))
    for i in node.next_nodes:
        retrieve_path(i, node.name, path)


def amr_reader(raw_amr):
    '''
    :param str raw_amr: input raw amr
    :return dict amr_nodes_acronym:
    :return list path:
    '''
    global amr_contents
    amr_contents = []
    amr_nodes_content = {} # Content as key
    amr_nodes_acronym = {} # Acronym as key
    path = [] # Nodes path

    split_amr(raw_amr, [])
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            generate_node_single(i, amr_nodes_content, amr_nodes_acronym)
    for i in amr_contents:
        if i.count('(') > 1 and i.count(')') > 1:
            generate_nodes_multiple(i, amr_nodes_content, amr_nodes_acronym)
    for i in amr_contents:
        if i.count('(') == 1 and i.count(')') == 1:
            revise_node(i, amr_nodes_content, amr_nodes_acronym)

    # The longest node (entire AMR) should be the root
    root = amr_nodes_content[sorted(amr_nodes_content, key=len, reverse=True)[0]]
    retrieve_path(root, '@', path)

    return amr_nodes_acronym, path


def main(raw_amrs):
    '''
    :param str raw_amrs: input raw amrs, separated by '\n'
    :return list res: Sentence objects
    '''
    res = []
    for i in re.split('\n\s*\n', raw_amrs):
        sent = re.search('::snt (.*?)\n', i)
        sent = sent.group(1) if sent else ''
        sentid = re.search('::id (.*?) ', i)
        if sentid:
            sentid = sentid.group(1)
        else:
            sentid = uuid.uuid4()

        raw_amr = ''
        comments = ''
        for line in i.splitlines(True):
            if line.startswith('# '):
                comments += line
                continue

            # convert '( )' to '%28 %29' in :wiki
            m = re.search(':wiki\s\"(.+?)\"', line)
            if m:
                line = line.replace(m.group(1),
                                    urllib.parse.quote_plus(m.group(1)))

            # convert '( )' to '%28 %29' in :name
            m = re.findall('\"(\S+)\"', line)
            for i in m:
                if '(' in i or ')' in i:
                    line = line.replace(i, urllib.parse.quote_plus(i))
            raw_amr += line

        if not raw_amr:
            continue
        if not amr_validator(raw_amr):
            raise Exception('Invalid raw AMR: %s' % sentid)

        amr_nodes_acronym, path = amr_reader(raw_amr)
        sent_obj = Sentence(sentid, sent, raw_amr, comments,
                            amr_nodes_acronym, path)
        res.append(sent_obj)

    return res
