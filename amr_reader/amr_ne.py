from namedentity import NamedEntity

'''
 generate AMR NamedEntity object
'''

'''
 AMR subtype to main type (PER, ORG, GPE) mapping table
'''
def get_subtype_mapping_table():
    import os
    currentpath = os.path.dirname(os.path.abspath(__file__))

    types = dict()
    f = open(currentpath + '/../doc/ne_types/isi_ne-type-sc.txt')
    for line in f:
        if '# superclass amr-ne-type' in line:
            continue
        line = line.strip().split(' ')
        types[line[1]] = line[0]
    return types

'''
 add NamedEntity object in to 'amr_table'
'''
def add_named_entity(amr_table):
    subtype_table = get_subtype_mapping_table()

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            sen = amr_table[docid][senid]
            amr_nodes_acr = sen.amr_nodes_

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
                    sen.named_entities_[node.name_] = ne
