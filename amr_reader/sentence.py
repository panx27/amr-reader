'''
 AMR Sentence Object
'''

class Sentence(object):
    def __init__(self, senid='', sen='', amr='',
                 amr_nodes=dict(),paths=list()):
        
        self.senid_ = senid         # sentence id
        self.sen_ = sen             # sentence
        self.amr_ = amr             # raw amr
        self.amr_nodes_ = amr_nodes # amr ndoes table
        self.paths_ = paths         # amr paths
        self.ne_queries = list()    # named entity queries


    def __str__(self):
        senid = '# ::id %s\n' % self.senid_
        sen = '# ::snt %s\n' % self.sen_
        amr = '%s\n' % self.amr_
        return senid + sen + amr
