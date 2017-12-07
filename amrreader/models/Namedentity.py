'''
 AMR Named Entity Object
'''

class NamedEntity(object):
    def __init__(self, sentid='', name='', entity_name='',
                 subtype=None, maintype=None, wiki=''):
        self.sentid = sentid           # Sentence id
        self.name = name               # Name (acronym)
        self.entity_name = entity_name # Full entity name
        self.subtype = subtype         # AMR sub-type
        self.maintype = maintype       # PER, ORG, GPE
        self.wiki = wiki               # Wikipedia title
        self.coreference = ''          # Coreferential name
        self.neighbors = set()         # AMR neighbors
        self.coherence = set()         # Coherent named entities
        self.chain = NamedEntity       # Coreferential chain

    def __str__(self):
        sentid = '# ::id %s\n' % self.sentid
        name = 'name: %s\n' % self.entity_name
        ne_type = 'entity type: %s\t%s\n' % (self.subtype, self.maintype)
        coreference = 'coreference: %s\n' % self.coreference
        wiki = '%s\n' % self.wiki
        return '%s' % (self.entity_name)

    def name(self):
        if self.coreference:
            return self.coreference
        else:
            return self.entity_name
