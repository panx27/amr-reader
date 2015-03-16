import re
import os
from namedentity import NamedEntity
# '''
#  Named Entity class
# '''
# class NameEntity(object):
#     def __init__(self, sen_id = '', acronym = '', 
#                  name = '', subtype = '', wiki = ''):
#         self.sen_id_ = sen_id
#         self.acronym_ = acronym
#         self.name_ = name
#         self.subtype_ = subtype
#         self.maintype_ = ''
#         if subtype in subtypes_table:
#             self.maintype_ = subtypes_table[subtype]
#         self.wiki_ = wiki
#         self.coreference_ = ''
#         self.attribute_ = set()
#         self.coherence_ = set()
#         self.path_ = list()

'''
 AMR adj. to nonu mapping table
'''
def get_adj_noun_mapping_table():
    # current_path = os.path.dirname(os.path.abspath(__file__))
    # f = open(current_path + '/doc/ne-table.txt')
    f = open('../doc/ne-table.txt')
    adj_noun_map = dict()
    for line in f:
        line = line.strip().split('\t')
        adj = line[0].lower() # LOWERCASE
        noun = line[1].lower()
        adj_noun_map[adj] = noun
    return adj_noun_map

'''
 AMR subtype to main type (PER, ORG, GPE) mapping table
'''
def get_subtype_mapping_table():
    # current_path = os.path.dirname(os.path.abspath(__file__))
    types = dict()
    # f = open(current_path + '/doc/ne_types/PER.txt')
    f = open('../doc/ne_types/PER.txt')
    for line in f:
        types[line.strip()] = 'PER'
    # f = open(current_path + '/doc/ne_types/ORG.txt')
    f = open('../doc/ne_types/ORG.txt')
    for line in f:
        types[line.strip()] = 'ORG'
    # f = open(current_path + '/doc/ne_types/GPE.txt')
    f = open('../doc/ne_types/GPE.txt')
    for line in f:
        types[line.strip()] = 'GPE'
    return types

# '''
#  named entity table

#  container: dict()   dict()  dict()  NameEntity
#  key:       docid -> senid -> ne ->  ne object
# '''
# def get_ne_table(root_to_entity):
#     ne_table = dict()
#     for i in root_to_entity.keys():
#         sen_id = i
#         doc_id = sen_id[:sen_id.rfind('.')]
#         if doc_id not in ne_table.keys():
#             ne_table[doc_id] = dict()
#         if sen_id not in ne_table[doc_id].keys():
#             ne_table[doc_id][sen_id] = dict()

#         for j in root_to_entity[i]:
#             entity = j[0].split('\t')
#             ne_abb = entity[0].replace('ENTITY:', '')
#             ne_type = entity[1]
#             ne_name = entity[2]
#             ne_wiki = entity[3]
#             if ne_abb not in ne_table[doc_id][sen_id].keys():
#                 ne_table[doc_id][sen_id][ne_abb] = NameEntity(sen_id,
#                                                                ne_abb,
#                                                                ne_name, 
#                                                                ne_type, 
#                                                                ne_wiki)
#     return ne_table



# adding entity to root path
def add_path(root_to_entity, ne_table):
    for i in root_to_entity.keys():
        sen_id = i
        doc_id = sen_id[:sen_id.rfind('.')]
        for j in root_to_entity[i]:
            entity = j[0].split('\t')
            ne_abb = entity[0].replace('ENTITY:', '')
            ne_type = entity[1]
            ne_name = entity[2]
            ne_wiki = entity[3]

            remaining = j[1:]
            try:
                assert len(remaining) % 2 == 0
            except AssertionError:
                print "ERROR: remaining is not even", name, remaining
            ne_table[doc_id][sen_id][ne_abb].path_.append(remaining)



# adding PER name coreference
def add_person_name_coreference(ne_table):
    for doc_id in ne_table.keys():
        name_entities_in_doc = list()
        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                name_entities_in_doc.append(ne_table[doc_id][sen_id][ne_abb])

        for i in name_entities_in_doc:
            ne_abb = i.acronym_
            sen_id = i.sen_id_
            doc_id = sen_id[:sen_id.rfind('.')]
            for j in name_entities_in_doc:
                ne_i = i.name_.split(' ')
                ne_j = j.name_.split(' ')
                ne_i_type = i.subtype_
                ne_j_type = j.subtype_
                # if the main type is PER, the number of tokens of mi is 1, 
                # and mi != mj, and mj contain mi, and sub-types of mi and mj are same
                if ne_i_type in subtypes_table.keys() and \
                   subtypes_table[ne_i_type] == "PER" and \
                   ne_j_type in subtypes_table.keys() and \
                   subtypes_table[ne_j_type] == "PER" and \
                   len(ne_i) == 1 and ne_i != ne_j and ne_i[0] in ne_j and \
                                              ne_i_type == ne_j_type:
                    ne_table[doc_id][sen_id][ne_abb].coreference_ = ' '.join(ne_j)



# adding ORG acronym coreference
def add_org_acronym_coreference(ne_table):
    for doc_id in ne_table.keys():
        name_entities_in_doc = list()
        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                name_entities_in_doc.append(ne_table[doc_id][sen_id][ne_abb])

        for i in name_entities_in_doc:
            # if all letters are uppercase, main type is ORG
            if i.name_.isupper() == True and \
               i.subtype_ in subtypes_table.keys() and \
               subtypes_table[i.subtype_] == "ORG":
                sen_id = i.sen_id_
                doc_id = sen_id[:sen_id.rfind('.')]
                acronym = i.name_
                for j in name_entities_in_doc:
                    if j.subtype_ in subtypes_table.keys() and \
                       subtypes_table[j.subtype_] == "ORG":
                        name = j.name_.split(' ')
                        if len(acronym) == len(name) and len(name) > 1:
                            match = True
                            for n in range(len(name)):
                                if name[n][0] != acronym[n]:
                                    match = False
                                    break
                            if match == True:
                                ne_table[doc_id][sen_id][i.acronym_].coreference_ = j.name_



def add_modify(modify, ne_table):
    for i in modify.keys():
        sen_id = i
        doc_id = sen_id[:sen_id.rfind('.')]
        for j in modify[i]:
            entity = j[0].split('\t')
            ne_abb = entity[0].replace('ENTITY:', '')
            ne_type = entity[1]
            ne_name = entity[2]
            ne_wiki = entity[3]
            
            remaining = j[1:]
            try:
                assert len(remaining) % 2 == 0
            except AssertionError: 
                print "ERROR: remaining is not even", sen_id, ne_name, remaining

            for r in zip(remaining, remaining[1:])[::2]:
                for r in zip(remaining, remaining[1:])[::2]:
                    try:
                        label = re.search("ROLE:(.+)", 
                                          r[0].strip()).group(1)
                        event = re.search("CONCEPT:(.+)|EVENT:(.+)", 
                                          r[1].strip()).group(1)
                    except AttributeError:
                        print "ERROR: cannot find label and event", ne_abb, r
                ne_table[doc_id][sen_id][ne_abb].attribute_.add((label, event))



def add_event(ne_table):
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id]:
            for ne_abb in ne_table[doc_id][sen_id]:
                for path in ne_table[doc_id][sen_id][ne_abb].path_:

                    for r in zip(path, path[1:])[::2]:
                        try:
                            label = re.search("ROLE:(.+)", 
                                              r[0].strip()).group(1)
                            event = re.search("EVENT:(.+)|ENTITY:(.+)", 
                                              r[1].strip()).group(1)
                        except AttributeError:
                            print "ERROR: cannot find label and event", ne_abb, r

                        ne_table[doc_id][sen_id][ne_abb].attribute_.add((label, event))
                        break # ONLY consider the closest role and event



def add_coherence(ne_table, conjunction = False):
    conjunction_list = ["and", "or", "contrast-01", "either", 
                        "neither", "slash", "between", "both"]
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id].keys():
            for m in ne_table[doc_id][sen_id].keys():
                for n in ne_table[doc_id][sen_id].keys():
                    m_paths = ne_table[doc_id][sen_id][m].path_
                    n_paths = ne_table[doc_id][sen_id][n].path_
                    for m_path in m_paths:
                        for n_path in n_paths:
                            if m != n and len(m_path) == len(n_path) and \
                               len(m_path) > 0 and m_path[1] == n_path[1] and \
                               'EVENT:' in m_path[0] and 'EVENT:' in n_path[0]:
                                try:
                                    event = re.search("EVENT:(.+)", m_path[1]).group(1)
                                except AttributeError:
                                    print "ERROR: canot find event\n%s\n%s\n%s\n\n" \
                                        % (sen_id, m_path, n_path)

                                coherent_name = ne_table[doc_id][sen_id][n].coreference_
                                if coherent_name == '':
                                    coherent_name = ne_table[doc_id][sen_id][n].name_
                                if conjunction:
                                    if event in conjunction_list:
                                        ne_table[doc_id][sen_id][m].coherence_.add \
                                            ((event, coherent_name))
                                else:
                                    ne_table[doc_id][sen_id][m].coherence_.add \
                                        ((event, coherent_name))



def add_haveorgrole91(have_org_role_91, ne_table):
    for i in have_org_role_91.keys():
        for j in have_org_role_91[i]:
            for k in j:
                if k[0] == ":ARG0" and "person\t" in k[1]:
                    title = ''
                    sen_id = i
                    doc_id = sen_id[:sen_id.rfind('.')]
                    entity = k[1].split('\t')
                    ne_abb = entity[0].replace('ENTITY:', '')
                    ne_type = entity[1]
                    ne_name = entity[2]
                    ne_wiki = entity[3]
                    ne_table[doc_id][sen_id][ne_abb].attribute_.add \
                        (("have-org-role-91", "office holder"))
                    for n in j:
                        if n[0] == ":ARG2":
                            m = re.match(".+-\d", n[1])
                            if m == None: # remvoe non title
                                ne_table[doc_id][sen_id][ne_abb].attribute_.add \
                                    (("have-org-role-91-title", n[1].strip()))
                    for n in j: # add coherence
                        if n[0] == ":ARG1" and "\t" in n[1]:
                            arg1_entity = n[1].split('\t')
                            arg1_ne_abb = arg1_entity[0].replace('ENTITY:', '')
                            arg1_ne_type = arg1_entity[1]
                            arg1_ne_name = arg1_entity[2]
                            arg1_ne_wiki = arg1_entity[3]
                            arg1_ne_name = arg1_ne_name.replace(": polarity -", "").strip()
                            if title == "": title = "office-holder"
                            ne_table[doc_id][sen_id][ne_abb].coherence_.add \
                                ((title, arg1_ne_name))
                            ne_table[doc_id][sen_id][arg1_ne_abb].coherence_.add \
                                (('have-org-role-91-arg0', ne_name))



# combine coherent entities in doc level
def combination_doc_level(ne_table):
    for doc_id in ne_table.keys():
        combination = dict()
        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                com_name = ne_table[doc_id][sen_id][ne_abb].coreference_
                if com_name == '':
                    com_name = ne_table[doc_id][sen_id][ne_abb].name_
                if com_name not in combination.keys():
                    combination[com_name] = NameEntity(name = com_name)
                combination[com_name].attribute_ = \
                combination[com_name].attribute_.union(ne_table[doc_id][sen_id][ne_abb].attribute_)
                combination[com_name].coherence_ = \
                combination[com_name].coherence_.union(ne_table[doc_id][sen_id][ne_abb].coherence_)

        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                com_name = ne_table[doc_id][sen_id][ne_abb].coreference_
                if com_name == '':
                    com_name = ne_table[doc_id][sen_id][ne_abb].name_
                ne_table[doc_id][sen_id][ne_abb].attribute_ = combination[com_name].attribute_
                ne_table[doc_id][sen_id][ne_abb].coherence_ = combination[com_name].coherence_



# combine coherent entities in discourse level
def combination_dis_level(ne_table):
    combination = dict()
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                com_name = ne_table[doc_id][sen_id][ne_abb].coreference_
                if com_name == '':
                    com_name = ne_table[doc_id][sen_id][ne_abb].name_
                if com_name not in combination.keys():
                    combination[com_name] = NameEntity(name = com_name)
                combination[com_name].attribute_ = \
                combination[com_name].attribute_.union(ne_table[doc_id][sen_id][ne_abb].attribute_)
                combination[com_name].coherence_ = \
                combination[com_name].coherence_.union(ne_table[doc_id][sen_id][ne_abb].coherence_)
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id].keys():
            for ne_abb in ne_table[doc_id][sen_id].keys():
                com_name = ne_table[doc_id][sen_id][ne_abb].coreference_
                if com_name == '':
                    com_name = ne_table[doc_id][sen_id][ne_abb].name_
                ne_table[doc_id][sen_id][ne_abb].attribute_ = combination[com_name].attribute_
                ne_table[doc_id][sen_id][ne_abb].coherence_ = combination[com_name].coherence_



def generator(input, coherence_level):
    raw_amr, root_to_entity, modify, have_org_role_91 = \
                                                        amr_reader.read(input)
    ne_table = get_ne_table(root_to_entity)
    add_path(root_to_entity, ne_table)
    add_person_name_coreference(ne_table)
    add_org_acronym_coreference(ne_table)
    add_event(ne_table)
    add_coherence(ne_table)
    add_haveorgrole91(have_org_role_91, ne_table)
    if coherence_level == 'doc':
        combination_doc_level(ne_table)
    elif coherence_level == 'dis':
        combination_dis_level(ne_table)
    return raw_amr, ne_table








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
            retrieve_path_rte(i, path, paths_rte)
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
            retrieve_path_etl(i, tmp, paths_etl)
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_etl(i, tmp, paths_etl)
    
def main(amr_table):
    print 'hehe'
    subtype_table = get_subtype_mapping_table()
    
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            named_entities = list() # 
            paths_rte = list() # path - root to entity
            paths_etl = list() # path - entity to leaf
            sen = amr_table[docid][senid]
            amr_nodes_acr = sen.amr_nodes_
            path_whole = sen.paths_[0]
            root = amr_nodes_acr[path_whole[0][1]]

            ### generate NamedEntity object
            for i in amr_nodes_acr:
                node = amr_nodes_acr[i]
                if node.is_entity_ and node.entity_type_ != '':
                    main_type = ''
                    if node.entity_type_ in subtype_table:
                        main_type = subtype_table[node.entity_type_]
                    ne = NamedEntity(senid=senid, name=node.name_,
                                     entity_name=node.entity_name_,
                                     subtype=node.entity_type_,
                                     maintype=main_type, wiki=node.wiki_)
                    # print ne
                    
            ### generate path - root to entity
            retrieve_path_rte(root, [('@root', root.ful_name_)], paths_rte)
            sen.paths_.append(paths_rte)
            # for i in paths_rte: print i

            ### generate path - entity to leaf
            for i in amr_nodes_acr:
                node = amr_nodes_acr[i]
                if node.is_entity_ and node.next_ != list():
                    ne = '%s\t%s' % (node.entity_type_, node.entity_name_)
                    retrieve_path_etl(node, [('@entity', ne)], paths_etl)
            sen.paths_.append(paths_etl)
            # for i in paths_etl: print i






            break
        break


            

    
if __name__ == "__main__":
    raw_amr, root_to_entity, modify, have_org_role_91 = \
                                                        amr_reader.read(open('./docs/test/tmp.txt').read())
    ne_table = get_ne_table(root_to_entity)
    add_path(root_to_entity, ne_table)
    add_person_name_coreference(ne_table)
    add_org_acronym_coreference(ne_table)
    add_event(ne_table)
    add_coherence(ne_table)
    add_haveorgrole91(have_org_role_91, ne_table)
    combination_doc_level(ne_table)
    # combination_dis_level(ne_table)

    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id]:
            for abb in ne_table[doc_id][sen_id]:
                print sen_id

                # print ne_table[doc_id][sen_id][abb].name_,
                # print ne_table[doc_id][sen_id][abb].coreference_

                # print ne_table[doc_id][sen_id][abb].name_
                # for p in ne_table[doc_id][sen_id][abb].path_:
                #     print p
                # print 

                # print ne_table[doc_id][sen_id][abb].name_,
                # print ne_table[doc_id][sen_id][abb].attribute_

                # print ne_table[doc_id][sen_id][abb].name_,
                # print ne_table[doc_id][sen_id][abb].coherence_

                # print ne_table[doc_id][sen_id][abb].name_,
                # print ne_table[doc_id][sen_id][abb].coreference_
                # print ne_table[doc_id][sen_id][abb].attribute_
                # print ne_table[doc_id][sen_id][abb].coherence_

                # if ne_table[doc_id][sen_id][abb].attribute_ != set():
                #     print sen_id
                #     print ne_table[doc_id][sen_id][abb].name_
                #     print ne_table[doc_id][sen_id][abb].attribute_
                #     print 
