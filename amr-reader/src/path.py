'''
 Generate AMR paths
'''

'''
 Retrieve path - root to entity
'''
def retrieve_path_rte(node, path, paths_rte, named_entities):
    for i in node.next_:
        tmp = path[:] # Passing by value
        if i.is_entity_:
            ne = named_entities[i.name_]
            path.append((i.edge_label_, ne))
            paths_rte.append(path)
            retrieve_path_rte(i, path, paths_rte, named_entities)
            path = tmp
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_rte(i, tmp, paths_rte, named_entities)

'''
 Retrieve path - entity to leaf
'''
def retrieve_path_etl(node, path, paths_etl, named_entities, amr_nodes):
    if node.next_ == list():
        paths_etl.append(path)
    for i in node.next_:
        tmp = path[:] # Passing by value
        if (i.is_entity_) or \
           (i.name_ in named_entities and i.ful_name_ == ''):
            ne = named_entities[i.name_]
            tmp.append((i.edge_label_, ne))
            retrieve_path_etl(i, tmp, paths_etl, named_entities, amr_nodes)
        else:
            if i.ful_name_ == '':
                if amr_nodes[i.name_].ful_name_ != '':
                    tmp.append((i.edge_label_, amr_nodes[i.name_].ful_name_))
                else:
                    tmp.append((i.edge_label_, i.name_)) # In case of :value
            else:
                tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_etl(i, tmp, paths_etl, named_entities, amr_nodes)

def main(amres):
    for snt in amres:
        amr_nodes = snt.amr_nodes_
        graph = snt.graph_
        root = amr_nodes[graph[0][1]]

        paths_rte = list() # Path - root to entity
        paths_etl = list() # Path - entity to leaf

        ### Generate path - root to entity
        retrieve_path_rte(root, [('@root', root.ful_name_)],
                          paths_rte, snt.named_entities_)
        if paths_rte != []:
            snt.amr_paths_['rte'] = paths_rte

        ### Generate path - entity to leaf
        for acr in amr_nodes:
            node = amr_nodes[acr]
            if node.is_entity_ and node.next_ != list():
                ne = snt.named_entities_[node.name_]
                retrieve_path_etl(node, [('@entity', ne)], paths_etl,
                                  snt.named_entities_, snt.amr_nodes_)
        if paths_etl != []:
            snt.amr_paths_['etl'] = paths_etl
