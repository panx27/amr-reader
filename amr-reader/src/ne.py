'''
 Generate AMR NamedEntity object
'''

from Namedentity import NamedEntity

'''
 AMR subtype to main type (PER, ORG, GPE) mapping table
'''
def get_subtype_mapping_table():
    import os
    currentpath = os.path.dirname(os.path.abspath(__file__))

    types = dict()
    f = open(currentpath + '/../docs/ne_types/isi_ne-type-sc.txt')
    for line in f:
        if '# superclass amr-ne-type' in line: # First line
            continue
        line = line.strip().split(' ')
        types[line[1]] = line[0]
    return types

'''
 Add NamedEntity object
'''
def add_named_entity(amres):
    sttable = get_subtype_mapping_table()
    for snt in amres:
        ### Generate NamedEntity object
        for acr in snt.amr_nodes_:
            node = snt.amr_nodes_[acr]
            if node.is_entity_:
                mtype = ''
                if node.entity_type_ in sttable:
                    mtype = sttable[node.entity_type_]
                ne = NamedEntity(senid=snt.senid_, name=node.name_,
                                 entity_name=node.entity_name_,
                                 subtype=node.entity_type_,
                                 maintype=mtype, wiki=node.wiki_)
                snt.named_entities_[node.name_] = ne
