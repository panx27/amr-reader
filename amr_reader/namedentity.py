'''
 AMR Named Entity Object
'''

class NamedEntity(object):
    def __init__(self, senid='', name='', entity_name='',
                 subtype='', maintype='', wiki=''):
        self.senid_ = senid             # sentence id
        self.name_ = name               # name (acronym)
        self.entity_name_ = entity_name # full entity name
        self.subtype_ = subtype         # amr sub-type
        self.maintype_ = maintype       # PER, ORG, GPE
        self.wiki_ = wiki               # wikipedia title
        self.coreference_ = ''          # coreference name
        self.attribute_ = set()         # amr attribute
        self.coherence_ = set()         # coherent named entity
        # self.paths_ = list()            # amr paths

    def __str__(self):
        senid = '# ::id %s\n' % self.senid_
        name = 'name: %s\n' % self.entity_name_
        ne_type = 'entity type: %s\t%s\n' % (self.subtype_, self.maintype_)
        coreference = 'coreference: %s\n' % self.coreference_
        wiki = '%s\n' % self.wiki_
        # return senid + name + ne_type + wiki
        return '%s' % (self.entity_name_)
        # return '%s, %s' % (self.entity_name_, self.coreference_)
