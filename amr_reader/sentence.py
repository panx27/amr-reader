'''
 AMR Sentence Object
'''

class Sentence(object):
    def __init__(self, senid='', sen='', amr='',
                 amr_nodes=dict(), path_whole=list()):
        
        self.senid_ = senid           # sentence id
        self.sen_ = sen               # sentence
        self.amr_ = amr               # raw amr
        self.amr_nodes_ = amr_nodes   # amr ndoes table
        self.path_whole_ = path_whole # path of whole graph
        self.amr_paths_ = dict()      # amr paths
        self.named_entities = dict()  # named entities

    def __str__(self):
        senid = '# ::id %s\n' % self.senid_
        sen = '# ::snt %s\n' % self.sen_
        amr = '%s\n' % self.amr_
        return senid + sen + amr
