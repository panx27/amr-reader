'''
 AMR Node Object
'''

class Node(object):
    def __init__(self, name='', ful_name='', next_node=list(), edge_label='',
                 is_entity=False, entity_type='', entity_name='', wiki='',
                 polarity=False):
        self.name_ = name               # Name of node (acronym)
        self.ful_name_ = ful_name       # Full name of node
        self.next_ = next_node          # Next nodes (a list)
        self.edge_label_ = edge_label   # Edge label between two nodes
        self.is_entity_ = is_entity     # Whether the node is named entity
        self.entity_type_ = entity_type # AMR type of entity
        self.entity_name_ = entity_name # Nname of entity
        self.wiki_ = wiki               # Wikipedia title of entity
        self.polarity_ = polarity       # Whether the node is polarity

    def __str__(self):
        if self.ful_name_ == '':
            name = 'NAME OF NODE: %s\n' % self.name_
        else:
            name = 'NAME OF NODE: %s / %s\n' % (self.name_, self.ful_name_)
        polarity = 'POLARITY: %s\n' % self.polarity_
        children = 'LINK TO:\n'
        for i in self.next_:
            if i.ful_name_ == '':
                children += '\t(%s) -> %s\n' % (i.edge_label_, i.name_)
            else:
                children += '\t(%s) -> %s / %s\n' % (i.edge_label_, i.name_,
                                                     i.ful_name_)
        if not self.is_entity_:
            return name + polarity + children
        else:
            m = 'ENTITY TYPE: %s\nENTITY NAME: %s\nWIKIPEDIA TITLE: %s\n' % \
                     (self.entity_type_, self.entity_name_, self.wiki_)
            return name + polarity + m + children
