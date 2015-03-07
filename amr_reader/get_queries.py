import re
import os
import amr_reader



# Name Entity class
class NameEntity(object):
    def __init__(self, sen_id = "", name = "", subtype = ""):
        self.sen_id_ = sen_id
        self.name_ = name
        self.subtype_ = subtype
        self.coreference_ = ""
        self.attribute_ = set()
        self.coherence_ = set()
        self.path_ = list()



# generate the adj. to nonu mapping table
def get_adj_noun_mapping_table():
    f = open("../docs/ne-table.txt")
    adj_noun_map = {}
    for line in f:
        line = line.strip().split("\t")
        adj = line[0].lower() # LOWERCASE
        noun = line[1].lower()
        adj_noun_map[adj] = noun
    return adj_noun_map
adj_noun_table = get_adj_noun_mapping_table()



# get subtype to main type (PER, ORG, GPE) mapping table
def get_subtype_mapping_table():
    types = {}
    f = open("../docs/ne_types/PER.txt")
    for line in f:
        types[line.strip()] = "PER"
    f = open("../docs/ne_types/ORG.txt")
    for line in f:
        types[line.strip()] = "ORG"
    f = open("../docs/ne_types/GPE.txt")
    for line in f:
        types[line.strip()] = "GPE"
    return types
subtypes_table = get_subtype_mapping_table()



# generate a sen_id and names entities table
# dict()    dict()   dict()  NameEntity
# doc_id -> sen_id -> ne -> the class of ne
def get_ne_table(path):
    f = open(path, 'r')
    f = f.read()
    f = f.split('# ::id ')
    f.remove("")

    ne_table = dict()
    for i in f:
        i = i.split('\n')
        sen_id = i[0]
        doc_id = sen_id[:sen_id.rfind('.')]
        if doc_id not in ne_table.keys():
            ne_table[doc_id] = dict()
        if sen_id not in ne_table[doc_id].keys():
            ne_table[doc_id][sen_id] = dict()
        for j in i[1:]:
            j = j.strip().split("\t")
            for k in j:
                if "ENTITY:" in k:
                    k = k.replace("ENTITY:", "")
                    ne_type = re.search("(\S+):\s", k).group(1)
                    k = k.replace(ne_type + ": ", "")
                    k = k.replace(": polarity -", "")
                    NE = k.strip() # real name
                    ne = k.strip().lower() # LOWERCASE
                    if ne not in ne_table[doc_id][sen_id].keys():
                        ne_table[doc_id][sen_id][ne] = NameEntity(sen_id, NE, ne_type)
    return ne_table



# adding PER name coreference
def add_person_name_coreference(ne_table):
    for doc_id in ne_table.keys():
        name_entities_in_doc = list()
        for sen_id in ne_table[doc_id].keys():
            for ne in ne_table[doc_id][sen_id].keys():
                name_entities_in_doc.append(ne_table[doc_id][sen_id][ne])

        for i in name_entities_in_doc:
            ne = i.name_.lower()
            sen_id = i.sen_id_
            doc_id = sen_id[:sen_id.rfind('.')]
            for j in name_entities_in_doc:
                ne_i = i.name_.split(' ')
                ne_j = j.name_.split(' ')
                ne_i_type = i.subtype_
                ne_j_type = j.subtype_
                # if the main type is PER, the number of tokens of mi is 1, 
                # and mi != mj, and mj contain mi, and sub-types of mi and mj are same
                if ne_i_type in subtypes_table.keys() and subtypes_table[ne_i_type] == "PER" \
                   and len(ne_i) == 1 and ne_i != ne_j and ne_i[0] in ne_j and ne_i_type == ne_j_type: 
                    ne_table[doc_id][sen_id][ne].coreference_ = ' '.join(ne_j)



# adding ORG acronym coreference
def add_org_acronym_coreference(ne_table):
    for doc_id in ne_table.keys():
        name_entities_in_doc = list()
        for sen_id in ne_table[doc_id].keys():
            for ne in ne_table[doc_id][sen_id].keys():
                name_entities_in_doc.append(ne_table[doc_id][sen_id][ne])

        for i in name_entities_in_doc:
            # if all letters are uppercase, main type is ORG
            if i.name_.isupper() == True and i.subtype_ in subtypes_table.keys() and subtypes_table[i.subtype_] == "ORG":
                sen_id = i.sen_id_
                doc_id = sen_id[:sen_id.rfind('.')]
                acronym = i.name_
                for j in name_entities_in_doc:
                    ne = j.name_.split(' ')
                    if len(acronym) == len(ne) and len(ne) > 1:
                        match = True
                        for n in range(len(ne)):
                            if ne[n][0] != acronym[n]:
                                match = False
                                break
                        if match == True:
                            ne_table[doc_id][sen_id][i.name_.lower()].coreference_ = j.name_



def add_haveorgrole91(ne_table):
    f = open("../output/amr_path/amr_entity_have_org_role", 'r')
    f = f.read()
    f = f.split('# ::id ')
    f.remove("")

    all_haveorgrole = dict()
    for i in f:
        haveorgrole = i.split('\n')
        sen_id = haveorgrole[0]
        if sen_id not in all_haveorgrole.keys():
            all_haveorgrole[sen_id] = list()
        c = list()
        for h in haveorgrole[1:]:
            if h != '':
                h = h.split('\t')
                role = h[0]
                concept = h[1]
                c.append((role, concept))
        all_haveorgrole[sen_id].append(c)

    for i in all_haveorgrole.keys():
        for j in all_haveorgrole[i]:
            for k in j:
                if k[0] == ":ARG0" and "person: " in k[1]:
                    title = ''
                    sen_id = i
                    doc_id = sen_id[:sen_id.rfind('.')]
                    ne_type = re.search("(\S+):\s", k[1]).group(1)
                    ne = k[1].replace(ne_type + ": ", "")
                    ne = ne.replace(": polarity -", "")
                    ne = ne.strip().lower()
                    ne_table[doc_id][sen_id][ne].attribute_.add(("have-org-role-91", "office holder"))
                    for n in j:
                        if n[0] == ":ARG2":
                            m = re.match(".+-\d", n[1]) 
                            if m == None: # remvoe non title
                                ne_table[doc_id][sen_id][ne].attribute_.add(("have-org-role-91-title", n[1].strip()))
                    for n in j: # add coherence
                        if n[0] == ":ARG1" and ": " in n[1]:
                            arg1_ne_type = re.search("(\S+):\s", n[1]).group(1)
                            arg1_ne = n[1].replace(arg1_ne_type + ": ", "")
                            arg1_ne = arg1_ne.replace(": polarity -", "").strip()
                            if title == "": title = "office-holder"
                            ne_table[doc_id][sen_id][ne].coherence_.add((title, arg1_ne))



def add_modify(ne_table):
    f = open("../output/amr_path/amr_entity_modify_path", 'r')
    f = f.read()
    f = f.split('# ::id ')
    f.remove("")

    for i in f:
        i = i.split('\n')
        sen_id = i[0]
        content = i[1]
        content = content
        content = content.strip().split("\t")
        name = content[0]
        remaining = content[1:]
        try:
            assert len(remaining) % 2 == 0
        except AssertionError:
            print "ERROR:odd concepts", name, remaining
            continue

        m = re.search("ENTITY:(.+): (.+)", name)
        ne_type = m.group(1)
        ne = m.group(2).lower()

        doc_id = sen_id[:sen_id.rfind('.')]
        for r in zip(remaining, remaining[1:])[::2]:
            # label = re.search("ROLE:(.+)" ,r[0].strip()).group(1)
            # # event = re.search("EVENT:(.+)|ENTITY:(.+)" ,r[1].strip()).group(1)
            # event = re.search("EVENT:(.+)" ,r[1].strip()).group(1)
            for r in zip(remaining, remaining[1:])[::2]:
                try:
                    label = re.search("ROLE:(.+)" ,r[0].strip()).group(1)
                    event = re.search("CONCEPT:(.+)|EVENT:(.+)" ,r[1].strip()).group(1)
                except AttributeError:
                    print "ERROR", ne, r

            ne_table[doc_id][sen_id][ne].attribute_.add((label, event))



def add_event(ne_table):
    f = open("../output/amr_path/amr_entity_to_root_path", 'r')
    f = f.read()
    f = f.split('# ::id ')
    f.remove("")

    for i in f:
        i = i.split('\n')
        sen_id = i[0]
        doc_id = sen_id[:sen_id.rfind('.')]
        for j in i[1:]:
            if j != "":
                j = j.strip().split("\t")
                name = j[0]
                remaining = j[1:]
                # m = re.search("ENTITY:(.+):* (.+)", name)
                m = re.search("ENTITY:(\S+): (.+)", name)
                ne_type = m.group(1)
                ne = m.group(2).lower()

                try:
                    assert len(remaining) % 2 == 0
                except AssertionError:
                    print "ERROR", ne, remaining
                try:
                    ne_table[doc_id][sen_id][ne].path_ = remaining
                except KeyError:
                    print sen_id, ne

                for r in zip(remaining, remaining[1:])[::2]:
                    try:
                        label = re.search("ROLE:(.+)", r[0].strip()).group(1)
                        event = re.search("EVENT:(.+)|ENTITY:(.+)", r[1].strip()).group(1)
                    except AttributeError:
                        print "ERROR", ne, r

                    ne_table[doc_id][sen_id][ne].attribute_.add((label, event))
                    break # ONLY consider the closest role and event



def add_coherence(ne_table):
    conjunction_list = ["and", "or", "contrast-01", "either", "neither", "slash", "between", "both"]
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id].keys():
            for m in ne_table[doc_id][sen_id].keys():
                for n in ne_table[doc_id][sen_id].keys():
                    m_path = ne_table[doc_id][sen_id][m].path_
                    n_path = ne_table[doc_id][sen_id][n].path_

                    if m != n and len(m_path) == len(n_path) and m_path[1] == n_path[1]:
                        if "EVENT" not in m_path[1] or "EVENT" not in n_path[1]:
                            continue
                        try:
                            event = re.search("EVENT:(.+)", m_path[1]).group(1)
                        except AttributeError:
                            print "ERROR"
                            print m, m_path
                            print n, n_path
                            print ""

                        # if the predicate event in conjunction list
                        if event in conjunction_list:
                            ne_table[doc_id][sen_id][m].coherence_.add((event, ne_table[doc_id][sen_id][n].name_))



def convert_coherence(coherence):
    if len(coherence) == 0:
        return ''
    else:
        result = ''
        for i in coherence:
            result += i[1] + ';'
        result = result.strip(';')
        return result



def convert_coherence_in_same_sentence(sentence, entity):
    result = ''
    for i in sentence:
        if i == entity:
            continue
        result += i + ';'
    result = result.strip(';')
    return result



if __name__ == "__main__":
    amr_reader.read()

    path = "../output/amr_path/amr_entity_to_root_path"
    ne_table = get_ne_table(path)
    add_person_name_coreference(ne_table)
    add_org_acronym_coreference(ne_table)
    add_haveorgrole91(ne_table)
    add_modify(ne_table)
    add_event(ne_table)
    add_coherence(ne_table)
    amr_types = set()

    out = open("../output/amr_entities", 'w')
    # out.write("sen_id,name,amr type,main type,coreference,coherence,coherence(in same sentence)\n")
    out.write("sen_id\tname\tamr type\tmain type\n")
    for doc_id in ne_table.keys():
        for sen_id in ne_table[doc_id].keys():
            for n in ne_table[doc_id][sen_id].keys():
                entity = ne_table[doc_id][sen_id][n]
                amr_types.add(entity.subtype_)
                if entity.subtype_ in subtypes_table.keys():
                    main_type = subtypes_table[entity.subtype_]
                else:
                    main_type = "OTHER"
                    
                # out.write("%s,%s,%s,%s,%s,%s,%s\n" % (entity.sen_id_, entity.name_, entity.subtype_, main_type, entity.coreference_, convert_coherence(entity.coherence_), convert_coherence_in_same_sentence(ne_table[doc_id][sen_id], n)))
                out.write("%s\t%s\t%s\t%s\n" % (entity.sen_id_, entity.name_, entity.subtype_, main_type))


    out2 = open("../output/amr_types", 'w')
    out2.write('%d\n' % len(amr_types))
    for i in sorted(amr_types):
        out2.write('%s\n' % i)
