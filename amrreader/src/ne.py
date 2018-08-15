import os

from .models.Namedentity import NamedEntity


def get_subtype_mapping_table():
    '''
    AMR subtype to main type (PER, ORG, GPE) mapping table

    :return dict mapping:
    '''
    currentpath = os.path.dirname(os.path.abspath(__file__))

    mapping = {}
    with open(currentpath+'/../static/ne_types/isi_ne-type-sc.txt', 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n').split()
            mapping[line[1]] = line[0]
    return mapping


def add_named_entity(sents):
    '''
    Add NamedEntity objects into Sentence objects

    :param Sentence_object sents: Sentence objects
    '''
    sttable = get_subtype_mapping_table()
    for snt in sents:
        for acr in snt.amr_nodes:
            node = snt.amr_nodes[acr]
            if node.is_entity:
                if node.entity_type in sttable:
                    maintype = sttable[node.entity_type]
                else:
                    maintype = None
                ne_obj = NamedEntity(sentid=snt.sentid, name=node.name,
                                     entity_name=node.entity_name,
                                     subtype=node.entity_type,
                                     maintype=maintype, wiki=node.wiki)
                snt.named_entities[node.name] = ne_obj
