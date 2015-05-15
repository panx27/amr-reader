'''
 AMR Sentence Object
'''

class Sentence(object):
    def __init__(self, senid='', sen='', amr='',
                 amr_nodes=dict(), graph=list()):
        self.senid_ = senid           # Sentence id
        self.sen_ = sen               # Sentence
        self.amr_ = amr               # Raw AMR
        self.amr_nodes_ = amr_nodes   # AMR ndoes table
        self.graph_ = graph           # Path of whole graph
        self.amr_paths_ = dict()      # AMR paths
        self.named_entities_ = dict() # Named entities

    def __str__(self):
        senid = '# ::id %s\n' % self.senid_
        sen = '# ::snt %s\n' % self.sen_
        amr = '%s\n' % self.amr_
        return senid + sen + amr
