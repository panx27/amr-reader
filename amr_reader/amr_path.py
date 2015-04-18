'''
 generate amr paths
'''

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

'''
 retrieve path - concept to leaf
'''
def retrieve_path_ctl(node, path, paths_ctl):
    if node.next_ == list():
        paths_ctl.append(path)
    for i in node.next_:
        tmp = path[:] # passing by value
        if i.is_entity_:
            ne = '%s\t%s' % (i.entity_type_, i.entity_name_)
            tmp.append((i.edge_label_, ne))
            retrieve_path_ctl(i, tmp, paths_ctl)
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_ctl(i, tmp, paths_ctl)

'''
 retrieve path - root to concept
'''
def retrieve_path_rtc(node, target, path, paths_rtc):
    if node.name_ == target:
        paths_rtc.append(path)

    for i in node.next_:
        tmp = path[:] # passing by value
        if i.is_entity_:
            # ne = '%s\t%s' % (i.entity_type_, i.entity_name_)
            # path.append((i.edge_label_, ne))
            # paths_rte.append(path)
            # retrieve_path_rte(i, path, paths_rte)
            # path = tmp
            ne = '%s\t%s' % (i.entity_type_, i.entity_name_)
            tmp.append((i.edge_label_, ne))
            retrieve_path_rtc(i, target, tmp, paths_rtc)
        else:
            tmp.append((i.edge_label_, i.ful_name_))
            retrieve_path_rtc(i, target, tmp, paths_rtc)
    
def add(amr_table):
    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            paths_rte = list() # path - root to entity
            paths_etl = list() # path - entity to leaf
            sen = amr_table[docid][senid]
            amr_nodes_acr = sen.amr_nodes_
            path_whole = sen.path_whole_
            root = amr_nodes_acr[path_whole[0][1]]

            ### generate path - root to entity
            retrieve_path_rte(root, [('@root', root.ful_name_)], paths_rte)
            sen.amr_paths_['rte'] = paths_rte
            # for i in paths_rte: print i

            ### generate path - entity to leaf
            for i in amr_nodes_acr:
                node = amr_nodes_acr[i]
                if node.is_entity_ and node.next_ != list():
                    ne = '%s\t%s' % (node.entity_type_, node.entity_name_)
                    retrieve_path_etl(node, [('@entity', ne)], paths_etl)
            sen.amr_paths_['etl'] = paths_etl
            # for i in paths_etl: print i

            ### generate path - entity to leaf
            paths_ctl = list()
            for i in amr_nodes_acr:
                node = amr_nodes_acr[i]
                if node.is_entity_ and node.next_ != list():
                    ne = '%s\t%s' % (node.entity_type_, node.entity_name_)
                    retrieve_path_ctl(node, [('@entity', ne)], paths_ctl)
            sen.amr_paths_['ctl'] = paths_ctl

            ### generate path - root to entity
            paths_rtc = list()
            retrieve_path_rtc(root, 'm', [('@root', root.ful_name_)], paths_rtc)
            sen.amr_paths_['rtc'] = paths_rtc

