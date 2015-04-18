'''
 AMR Node Object
'''

class Node(object):
    def __init__(self, name='', ful_name='', next_node=list(), edge_label='',
                 is_entity=False, entity_type='', entity_name='', wiki='',
                 is_polarity=False):
        self.name_ = name               # name of node (acronym)
        self.ful_name_ = ful_name       # full name of node
        self.next_ = next_node          # next nodes (a list)
        self.edge_label_ = edge_label   # edge label between two nodes
        self.is_entity_ = is_entity     # whether the node is named entity
        self.entity_type_ = entity_type # amr type of entity
        self.entity_name_ = entity_name # name of entity
        self.wiki_ = wiki               # wikipedia title of entity
        self.is_polarity_ = is_polarity # whether the node is polarity

    def __str__(self):
        name = 'NAME OF NODE: %s / %s\n' % (self.name_, self.ful_name_)
        polarity = 'POLARITY: %s\n' % self.is_polarity_
        children = 'LINK TO:\n'
        for i in self.next_:
            children += '\t(%s) -> %s / %s\n' % (i.edge_label_,
                                                 i.name_, i.ful_name_)
        if not self.is_entity_:
            return name + polarity + children
        else:
            m = 'ENTITY TYPE: %s\nENTITY NAME: %s\nWIKIPEDIA TITLE: %s\n' % \
                     (self.entity_type_, self.entity_name_, self.wiki_)
            return name + polarity + m + children
