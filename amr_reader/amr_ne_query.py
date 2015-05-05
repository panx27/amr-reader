'''
 generate AMR named entity query
'''
import copy
import re

'''
 adding name coreference
'''
def add_name_coreference(amr_table):
    for docid in sorted(amr_table):
        named_entities_doc_level = list()
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            for i in sen.named_entities_:
                ne = sen.named_entities_[i]
                named_entities_doc_level.append(ne)

        '''        
         PER name coreference:
           main type is PER;
           subtypes of mi and mj are same;
           mi != mj;
           number of tokens of mi is 1;
           mj contain mi;
        '''
        for i in named_entities_doc_level:
            if i.maintype_ != 'PER': continue
            for j in named_entities_doc_level:
                if i.subtype_ == j.subtype_ and i.entity_name_ != j.entity_name_:
                    namei = i.entity_name_.split(' ')
                    namej = j.entity_name_.split(' ')
                    if len(namei) == 1 and namei[0] in namej:
                        ne = amr_table[docid][i.senid_].named_entities_[i.name_]
                        ne.coreference_ = j.entity_name_

        '''        
         ORG name coreference:
           main type is ORG;
           capital letters;
           subtypes of mi and mj are same;
        '''
        for i in named_entities_doc_level:
            if i.maintype_ != 'ORG': continue
            if i.entity_name_.isupper() != True: continue
            for j in named_entities_doc_level:
                if i.subtype_ == j.subtype_:
                    namei = i.entity_name_
                    namej = j.entity_name_.split(' ')
                    if len(namei) == len(namej) and len(namej) > 1:
                            match = True
                            for n in range(len(namej)):
                                if namej[n][0] != namei[n]:
                                    match = False
                                    break
                            if match == True:
                                ne = amr_table[docid][i.senid_].named_entities_[i.name_]
                                ne.coreference_ = j.entity_name_

'''
 adding coherent set
'''
def add_coherence(amr_table):
    '''
     if one node links to multiple named entity nodes,
     those named entity nodes are considered as coherence
    '''
    # conjunction_list = ["and", "or", "contrast-01", "either", 
    #                     "neither", "slash", "between", "both"]
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_
            for n in amr_nodes:
                node = amr_nodes[n]
                tmp = list()
                for i in node.next_:
                    if i.is_entity_:
                        tmp.append((node, i.edge_label_, sen.named_entities_[i.name_]))

                for i in tmp:
                    ne = i[2]
                    for j in tmp:
                        if i != j:
                            node_name = j[0].ful_name_
                            edge_label = j[1]
                            coherent_ne = j[2]
                            ne.coherence_.add((node_name, edge_label, coherent_ne))

'''
 search :ARGn-of
'''
def search_argnof(node, amr_nodes):
    for i in amr_nodes:
        for j in amr_nodes[i].next_:
            if j.name_ == node.name_:
                m = re.search('(:ARG\d)-of' ,j.edge_label_)
                if m != None:
                    tmp = copy.copy(amr_nodes[i])
                    tmp.edge_label_ = m.group(1)
                    tmp.next_ = list()
                    node.next_.append(tmp)

'''
 adding special role:
   have-org-role-91
'''
def add_haveorgrole91(amr_table):
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_
            named_entities = sen.named_entities_

            ### have-org-role-91
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.ful_name_ != 'have-org-role-91':
                    continue
                else:
                    search_argnof(node, amr_nodes)
                    haveorgrole91 = dict()
                    for i in node.next_:
                        haveorgrole91[i.edge_label_] = i
                    if ':ARG0' in haveorgrole91:
                        arg0 = haveorgrole91[':ARG0']
                        if arg0.is_entity_:
                            organization = ''
                            title = ''
                            per = named_entities[arg0.name_]
                            per.neighbors_.add(('have-org-role-91:arg0', 'office holder'))
                            if ':ARG1' in haveorgrole91:
                                arg1 = haveorgrole91[':ARG1']
                                if arg1.is_entity_:
                                    org = named_entities[arg1.name_]
                                    organization = org.entity_name_
                                    ### adding coherence set
                                    per.coherence_.add(('have-org-role-91', ':ARG1', org))
                                    org.coherence_.add(('have-org-role-91', ':ARG0', per))
                                else:
                                    organization = arg1.ful_name_
                                per.neighbors_.add(('have-org-role-91:arg1', organization))

                            if ':ARG2' in haveorgrole91:
                                arg2 = haveorgrole91[':ARG2']
                                title = arg2.ful_name_ # TO-DO::id DF-202-185837-43_8915.18 :ARG2 is a subtree
                                per.neighbors_.add(('have-org-role-91:arg2', title))
                                
                            if organization != '' and title != '':
                                per.neighbors_.add(('have-org-role-91:arg1+arg2', organization+' '+title))

'''
 adding special role:
   have-rel-role-91
'''
def add_haverelrole91(amr_table):
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_
            named_entities = sen.named_entities_

            ### have-rel-role-91
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.ful_name_ != 'have-rel-role-91':
                    continue
                else:
                    search_argnof(node, amr_nodes)
                    haverelrole91 = dict()
                    for i in node.next_:
                        haverelrole91[i.edge_label_] = i
                    if ':ARG0' in haverelrole91 and ':ARG1' in haverelrole91:
                        arg0 = haverelrole91[':ARG0']
                        arg1 = haverelrole91[':ARG1']
                        if arg0.is_entity_ and arg1.is_entity_:
                            rel = 'have-rel-role-91'
                            if ':ARG2' in haverelrole91:
                                rel = haverelrole91[':ARG2'].ful_name_
                            ### adding coherence set
                            arg0_ne = named_entities[arg0.name_]
                            arg1_ne = named_entities[arg1.name_]
                            arg0_ne.coherence_.add(('have-rel-role-91', rel, arg1_ne))
                            arg1_ne.coherence_.add(('have-rel-role-91', rel, arg0_ne))

'''
 convert cardinal number to ordinal number
'''
def cardinal_to_ordinal(num):
    if num[-1] == '1':
        return num + 'st'
    if num[-1] == '2':
        return num + 'nd'
    if num[-1] == '3':
        return num + 'rd'
    else:
        return num + 'th'

'''
 adding global time
'''
def add_date_entity(amr_table):
    num_to_month = dict()
    months = ['January', 'February', 'March', 'April', 'May', 'June', \
              'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(1, 13):
        num_to_month[str(i)] = months[i-1]

    for docid in sorted(amr_table):
        ### find global time in doc level
        global_time_doc_level = set()
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_

            ### date-entity
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.ful_name_ != 'date-entity':
                    continue
                else:
                    time = ''
                    year = ''
                    month = ''
                    day = ''
                    date_entity = dict()
                    for i in node.next_:
                        date_entity[i.edge_label_] = i

                    ### date: month/day/yaer
                    if ':year' in date_entity:
                        year = date_entity[':year'].name_
                    if ':month' in date_entity:
                        month = date_entity[':month'].name_
                    if ':day' in date_entity:
                        day = date_entity[':day'].name_
                    if year != '' and month != '' and day != '':
                        date = '%s/%s/%s' % (month, day, year)
                        global_time_doc_level.add(('global-time', date))
                        try:
                            date = '%s %s %s' % (num_to_month[month], cardinal_to_ordinal(day), year)
                            global_time_doc_level.add(('global-time', date))
                        except:
                            pass
                    elif month != '' and day != '':
                        date = '%s/%s' % (month, day)
                        global_time_doc_level.add(('global-time', date))
                        try:
                            date = '%s %s' % (num_to_month[month], cardinal_to_ordinal(day))
                            global_time_doc_level.add(('global-time', date))
                        except:
                            pass
                    elif year != '':
                        date = year
                        global_time_doc_level.add(('global-time', date))

                    ### other
                    if ':century' in date_entity:
                        m = re.search('(\d\d)\d*', date_entity[':century'].name_)
                        if m != None:
                            time = cardinal_to_ordinal(m.group(1)) + ' century'
                    if ':weekday' in date_entity:
                        time = date_entity[':weekday'].ful_name_
                    if ':season' in date_entity:
                        time = date_entity[':season'].ful_name_
                    if ':decade' in date_entity:
                        time = date_entity[':decade'].name_
                    if time != '':
                        global_time_doc_level.add(('global-time', time))
        ### propagate
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            named_entities = sen.named_entities_
            for n in named_entities:
                ne = named_entities[n]
                if global_time_doc_level != set():
                    ne.neighbors_ = ne.neighbors_.union(global_time_doc_level)

'''
 adding global location
'''
def add_location(amr_table):
    for docid in sorted(amr_table):
        ### find global location in doc level
        global_loc_doc_level = set()
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_
            named_entities = sen.named_entities_

            ### :location
            for n in amr_nodes:
                node = amr_nodes[n]
                if node.edge_label_ != ':location':
                    continue
                else:
                    for i in node.next_:
                        if i.is_entity_:
                            ne = named_entities[i.name_]
                            global_loc_doc_level.add(('global-loc', ':location', ne))
        ### propagate
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            for n in named_entities:
                ne = named_entities[n]
                if global_loc_doc_level != set():
                    ne.coherence_ = ne.coherence_.union(global_loc_doc_level)

'''
 retrieve AMR subtree - concept to leaf
'''
def retrieve_ctl(node, path, paths_ctl, named_entities, amr_nodes):
    tmp = path[:] # passing by value
    if (node.is_entity_) or \
       (node.name_ in named_entities and node.ful_name_ == ''):
        ne = named_entities[node.name_]
        tmp.append((node.edge_label_, ne))
    else:
        if node.ful_name_ == '':
            if amr_nodes[node.name_].ful_name_ != '':
                tmp.append((node.edge_label_, amr_nodes[node.name_].ful_name_))
            else:
                tmp.append((node.edge_label_, node.name_)) # in case of :value
        else:
            tmp.append((node.edge_label_, node.ful_name_))

    if node.next_ == list():
        paths_ctl.append(tmp)
    for i in node.next_:
        retrieve_ctl(i, tmp, paths_ctl, named_entities, amr_nodes)

'''
 adding semantic role
'''
def add_semantic_role(amr_table):
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes = sen.amr_nodes_
            named_entities = sen.named_entities_

            for n in amr_nodes:
                node = amr_nodes[n]
                for i in node.next_:
                    if i.is_entity_:
                        for j in node.next_:
                            if i != j:
                                paths_ctl = list()
                                retrieve_ctl(j, list(), paths_ctl, named_entities, amr_nodes)
                                ne = named_entities[i.name_]
                                for path in paths_ctl:
                                    for k in path:
                                        if isinstance(k[1], str): # node
                                            ne.neighbors_.add(k)
                                        else:                     # named entity
                                            ne.coherence_.add((node.ful_name_, k[0], k[1]))

'''
 merge coreferential named entities as a coreferential chian in doc level
'''
def get_chain_doc_level(amr_table):
    from namedentity import NamedEntity

    for docid in sorted(amr_table):
        chain = dict()
        ### merge
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            for i in sen.named_entities_:
                ne = sen.named_entities_[i]
                name = ne.name()
                if name not in chain: # key should be entity name + entity type?
                    chain[name] = NamedEntity(entity_name=name, subtype=ne.subtype_, 
                                              maintype=ne.maintype_, wiki=ne.wiki_)
                chain[name].neighbors_ = chain[name].neighbors_.union(ne.neighbors_)
                chain[name].coherence_ = chain[name].coherence_.union(ne.coherence_)

        ### propagate
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            for i in sen.named_entities_:
                ne = sen.named_entities_[i]
                name = ne.name()
                ne.neighbors_ = chain[name].neighbors_
                ne.coherence_ = chain[name].coherence_

def main(amr_table, chain=True):
    ### adding name coreference
    add_name_coreference(amr_table)

    ### adding coherent set
    add_coherence(amr_table)

    ### adding have-org-rol-91
    add_haveorgrole91(amr_table)

    ### adding have-rel-rol-91
    # add_haverelrole91(amr_table)

    ### adding global time
    add_date_entity(amr_table)

    ### adding global location
    add_location(amr_table)

    ### adding semantic role
    add_semantic_role(amr_table)
    
    ### adding coreferential chain
    if chain:
        get_chain_doc_level(amr_table)
