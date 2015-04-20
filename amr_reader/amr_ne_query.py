'''
 generate AMR named entity query
'''

'''
 AMR adj. to nonu mapping table
'''
def get_adj_noun_mapping_table():
    f = open('../doc/ne-table.txt')
    adj_noun_map = dict()
    for line in f:
        line = line.strip().split('\t')
        adj = line[0].lower() # LOWERCASE
        noun = line[1].lower()
        adj_noun_map[adj] = noun
    return adj_noun_map

'''
 adding name coreference
'''
def add_name_coreference(amr_table):
    for docid in sorted(amr_table):
        named_entities_doc_level = list()
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            for ne in sen.named_entities_:
                named_entities_doc_level.append(sen.named_entities_[ne])

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
                    if i.is_entity_ and i.entity_type_ != '':
                        tmp.append((node, i.edge_label_, sen.named_entities_[i.name_]))

                for i in tmp:
                    ne = i[2]
                    for j in tmp:
                        if i != j:
                            node_name = j[0].ful_name_
                            edge_label = j[1]
                            coherent_ne = j[2]
                            ne.coherence_.add((node_name, edge_label, coherent_ne))

def main(amr_table):
    import amr_paths
    amr_paths.main(amr_table)

    ### adding name coreference
    add_name_coreference(amr_table)

    ### adding coherent set
    add_coherence(amr_table)
