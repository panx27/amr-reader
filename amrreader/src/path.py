def retrieve_path_rte(node, path, paths_rte, named_entities):
    '''
     Retrieve path - root to entity
    '''
    for i in node.next_nodes:
        tmp = path[:] # Passing by value
        if i.is_entity:
            ne = named_entities[i.name]
            path.append((i.edge_label, ne))
            paths_rte.append(path)
            retrieve_path_rte(i, path, paths_rte, named_entities)
            path = tmp
        else:
            tmp.append((i.edge_label, i.ful_name))
            retrieve_path_rte(i, tmp, paths_rte, named_entities)

def retrieve_path_etl(node, path, paths_etl, named_entities, amr_nodes):
    '''
    Retrieve path - entity to leaf
    '''
    if node.next_nodes == []:
        paths_etl.append(path)
    for i in node.next_nodes:
        tmp = path[:] # Passing by value
        if (i.is_entity) or \
           (i.name in named_entities and i.ful_name == ''):
            ne = named_entities[i.name]
            tmp.append((i.edge_label, ne))
            retrieve_path_etl(i, tmp, paths_etl, named_entities, amr_nodes)
        else:
            if i.ful_name == '':
                if amr_nodes[i.name].ful_name:
                    tmp.append((i.edge_label, amr_nodes[i.name].ful_name))
                else:
                    tmp.append((i.edge_label, i.name)) # In case of :value
            else:
                tmp.append((i.edge_label, i.ful_name))
            retrieve_path_etl(i, tmp, paths_etl, named_entities, amr_nodes)


def main(sents):
    for snt in sents:
        amr_nodes = snt.amr_nodes
        graph = snt.graph
        root = amr_nodes[graph[0][1]]

        paths_rte = list() # Path - root to entity
        paths_etl = list() # Path - entity to leaf

        # Generate path - root to entity
        retrieve_path_rte(root, [('@root', root.ful_name)],
                          paths_rte, snt.named_entities)
        if paths_rte:
            snt.amr_paths['rte'] = paths_rte

        # Generate path - entity to leaf
        for acr in amr_nodes:
            node = amr_nodes[acr]
            if node.is_entity and node.next_nodes:
                ne = snt.named_entities[node.name]
                retrieve_path_etl(node, [('@entity', ne)], paths_etl,
                                  snt.named_entities, snt.amr_nodes)
        if paths_etl:
            snt.amr_paths['etl'] = paths_etl
