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
        self.neighbors_ = set()         # amr neighbors
        self.coherence_ = set()         # coherent named entities

    def __str__(self):
        senid = '# ::id %s\n' % self.senid_
        name = 'name: %s\n' % self.entity_name_
        ne_type = 'entity type: %s\t%s\n' % (self.subtype_, self.maintype_)
        coreference = 'coreference: %s\n' % self.coreference_
        wiki = '%s\n' % self.wiki_
        return '%s' % (self.entity_name_)
        # return '%s, %s, %s, %s' % (self.entity_name_, self.coreference_,
        #                            self.neighbors_, self.coherence_)

    def name(self):
        if self.coreference_ != '':
            return self.coreference_
        else:
            return self.entity_name_
