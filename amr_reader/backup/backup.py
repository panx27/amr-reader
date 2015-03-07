# '''
#  functionality: find acronym of nodes and their corresponding names
#  container: dict; key: acronym, value: full_name; 'amr_acronyms'
#  ex. amr_acronyms['b'] = 'boy'
#      amr_acronyms['b2'] = 'believe-01'
# '''
# def get_acronyms_table():
#     amr_acronyms = dict()
#     for i in amr_contents:
#         m = re.search('\S+\s/\s\S+', i[1:-1])
#         if m != None:
#             m = m.group().split(' / ')
#             amr_acronyms[m[0]] = m[1].strip()
#     return amr_acronyms




# # generate nodes function
# def generate_node(content, all_nodes):
#     backup_content = content # keep an orignal content as key 
#                              # of all_nodes(dict)

#     if content.count('(') >= 1:
#         all_arg_nodes = []
#     #--------------------------------------------------------------------
#     # in case of already existing nodes
#     # remove existing content and point to the particular node

#         # always check the longest content first
#         for i in sorted(all_nodes, key = len, reverse = True): 
#             if i in content:
#                 e = content.find(i)
#                 s = content[:e].rfind(':')
#                 relation = re.search(':\S+\s', content[s:e]).group()
#                 content = content.replace(relation + i, '', 1)
#                 all_nodes[i].edge_label_ = relation
#                 all_arg_nodes.append(all_nodes[i])
#     #---------------------------------------------------------------------
#         EVENT = re.search('\w+\s/\s\S+', content).group().split(' / ')[0]

#         args = re.findall(':\S+\s\(\w+\s/\s\S+\)|:\w+\s\w+', content)
#         names = re.findall(':op\d\s\'\S+\'', content)

#         for index, item in enumerate(args):
#             relation = re.search(':\S+\s', item).group() # relation is edge label
#             item = item.replace(relation, '')
#             concept = '' # concept is leaf
#             # no parenthesis
#             if item.count('(') == 0: # in case of ':ARG1 b'
#                 concept = str(item)
#             # single parenthesis
#             if item.count('(') == 1 and ':' not in item: # in case of 
#                                                          # ':ARG0 (g / girl)'
#                 concept = str(item[1:-1].split(' / ')[0])
#             all_arg_nodes.append(Node(name = concept, edge_label = relation))

#         is_entity = False
#         new_node = Node()
#         if ':name' in content and len(names) > 0:
#             if re.match('\S+\s/\s\S+\s.*:wiki\s-', content) != None:
#                 wikititle = '-'
#             else:
#                 m = re.search('\S+\s/\s\S+\s.*:wiki\s\'(.+?)\'', content)
#                 if m != None:
#                     wikititle = m.group(1)
#                 else:
#                     wikititle = 'None'

#             entity_name = ''
#             for i in names:
#                 entity_name += re.match(':op\d\s\'(\S+)\'', i).group(1) + ' '
#             new_node = Node(name = entity_name, ne = all_arg_nodes, 
#                             entity_type = EVENT, is_entity = True, wiki = wikititle)
#             all_nodes[backup_content] = new_node
#             global entity_list
#             entity_list.append(EVENT)  # EVENT is entity's type here
#             is_entity = True
#         if len(all_arg_nodes) > 0 and is_entity == False:
#             new_node = Node(name = EVENT, ne = all_arg_nodes)
#             all_nodes[backup_content] = new_node

#         global root
#         root = new_node # the last node is always the root




    
# # retrieve path function - entity to leaf
# def retrieve_path_entity_to_leaf(node, edges, path, added_edges):
#     # print node
#     if node[2] == 'entity':
#         e = all_acronyms[node[1]].strip()
#         e = e.split('\t')
#         path.append('ENTITY:' + all_acronyms[node[1]].strip())
#         added_edges.append(node)
#         # if node[3] != '':
#         #     path.append('ROLE' + node[3])
#     elif node[2] == 'event':
#         # if '-POLARITY-' in node[1]:
#         #     path.append('EVENT:' + all_acronyms[node[1].replace('-POLARITY-', '')] + '-P')
#         # else:
#         #     path.append('EVENT:' + all_acronyms[node[1]])
#         if node[3] != '':
#             path.append('ROLE' + node[3])
#         path.append('EVENT:' + all_acronyms[node[1]])
#         added_edges.append(node)
#     elif node[2] == '':
#         if node[3] != '':
#             path.append('ROLE' + node[3])
#         if node[1] in all_acronyms.keys():
#             path.append('CONCEPT:' + all_acronyms[node[1]])
#             entities_path.append(path)
#         else:
#             path.append('CONCEPT:' + node[1])
#             entities_path.append(path)
#         added_edges.append(node)

#     for i in edges:
#         if i[0] == node[1]:
#             if i in added_edges:
#                 continue
#             retrieve_path_entity_to_leaf(i, edges, path[:], added_edges)



# # retrieve path function - have-org-role-91
# def retrieve_path_have_org_role_91(edges):
#     all_have_org = set()
#     for e in edges:
#         if e[0] == '@':
#             continue
#         if all_acronyms[e[0]] == 'have-org-role-91':
#             all_have_org.add(e[0])

#     all_have_org_edges = dict()
#     for i in all_have_org:
#         connected_edges = list()
#         for e in edges:
#             if e[0] == i or e[1] == i:
#                 connected_edges.append(e)
#         all_have_org_edges[i] = connected_edges

#     return all_have_org_edges



# # retrieve path function - location
# def retrieve_path_location(edges):
#     locations = set()
#     for e in edges:
#         if e[3].strip() == ':location' and e[2] == 'entity':
#             name = all_acronyms[e[1]]
#             locations.add(('location', name))
#     return locations



# def read(input):
#     # f = open(input_file, 'r')
#     # sentences = f.read().strip().split('# ::id ')
#     sentences = input.strip().split('# ::id ')
#     # print sentences[0]
#     sentences = sentences[1:] # remove file title
#     raw_amr = list()
#     for i in sentences:
#         nline = i.split('\n')
#         senid = nline[0][:nline[0].find(' ')]
#         date = '# ::id %s' % nline[0]
#         sen = nline[1]
#         save = nline[2]
#         amr = '\n'.join(nline[3:]).strip()
#         raw_amr.append((senid, date, sen, save, amr))
    
#     root_to_entity = dict()
#     modify = dict()
#     have_org_role_91 = dict()
#     for i in raw_amr:
#         global all_contents
#         all_contents = []
#         global edges
#         edges = []
#         global entities_path
#         entities_path = []

#         sen_id = i[0]
#         doc_id = sen_id[:sen_id.rfind('.')]
#         # print sen_id

#         # combine amr annotation to one string 
#         amr_input = i[4].split('\n')
#         text = ''
#         for line in amr_input:
#             text += line.strip() + ' '
#         text = text[:-1]

#         if amr_validator(text) == False:
#             raise NameError('Invalid AMR Input: %s' % sen_id)

#         # run the recursion function
#         split(text, [])
#         all_contents.sort(key = len)

#         # generate acronyms table
#         global all_acronyms
#         all_acronyms = get_acronyms_table()

        # # generate node
        # all_nodes = {}
        # global entity_list
        # entity_list = []
        # for i in all_contents:
        #     if i.count('(') >= 1 and ':' in i:
        #         generate_node(i, all_nodes)
        #     elif len(all_contents) == 1:
        #         generate_node(i, all_nodes)

#         retrieve_node(root)

#         # root to entity
#         for i in edges:
#             if i[2] == 'entity':
#                 p = []
#                 retrieve_path_entity_to_root(i, edges, p)
#                 entities_path.append(p)
#         if entities_path != []:
#             if sen_id not in root_to_entity:
#                 root_to_entity[sen_id] = list()
#             for i in entities_path:
#                 root_to_entity[sen_id].append(i)
            
#         # modify
#         entities_path = []
#         for i in edges:
#             if i[2] == 'entity':
#                 p = []
#                 added_edges = []
#                 retrieve_path_entity_to_leaf(i, edges[edges.index(i):], 
#                                              p, added_edges)
#         if entities_path != []:
#             for i in entities_path:
#                 if len(i) > 1 and i[1] == 'ROLE:mod ':
#                     if sen_id not in modify:
#                         modify[sen_id] = list()
#                     modify[sen_id].append(i)

#         # have org role 91
#         hor91 = retrieve_path_have_org_role_91(edges)
#         for i in hor91.keys():
#             if sen_id not in have_org_role_9z1:
#                 have_org_role_91[sen_id] = list()
#             hor91_path = list()
#             for j in hor91[i]:
#                 if j[0] == '@': 
#                     continue
#                 l1 = j[3].strip().replace(':ARG0-of', ':ARG0')
#                 if 'ARG' not in l1:
#                     continue
#                 if j[0] != i and j[0] != 'interrogative':
#                     r1 = all_acronyms[j[0]]
#                 if j[1] != i and j[1] != 'interrogative':
#                     r1 = all_acronyms[j[1]]
#                 hor91_path.append((l1, r1))
#             have_org_role_91[sen_id].append(hor91_path)

#         # # location
#         # locations = retrieve_path_location(edges)
#         # for l in locations:
#         #     out4.write('@@@%s\n' % sen_id)
#         #     out4.write('%s, %s\n' % (l[0], l[1]))
#         #     out4.write('\n')

#         # # time
#         # date_entities = re.findall('\(d\d* \/ date-entity .*?\)', text)
#         # if len(date_entities) > 0:
#         #     out5.write('@@@%s\n' % sen_id)
#         #     for d in date_entities:
#         #         if d.count('(') == d.count(')'):
#         #             out5.write('%s\n' % d)
#         #         else:
#         #             n = text.find(d) + len(d)
#         #             while d.count('(') != d.count(')'):
#         #                 d += text[n]
#         #                 n += 1
#         #             out5.write('%s\n' % d)
#         #     out5.write('\n')

#     return raw_amr, root_to_entity, modify, have_org_role_91



# if __name__ == '__main__':
#     # read('tmp.txt')
#     read(open('default_input').read())
