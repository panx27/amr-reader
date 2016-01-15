import reader
import linkipedia

def wikify(amres):
    for snt in amres:
        for acr in snt.amr_nodes_:
            node = snt.amr_nodes_[acr]
            if node.is_entity_:
                lres = linkipedia.linking(node.entity_name_)
                if lres != list():
                    wiki = lres[0]
                else:
                    wiki = '-'
                con = '%s / %s' % (node.name_, node.ful_name_,)
                newcon = '%s / %s :wiki "%s"' % (node.name_,
                                                 node.ful_name_, wiki)
                snt.amr_ = snt.amr_.replace(con, newcon)
    return amres

if __name__ == '__main__':
    indir = '/Users/panx/Desktop/test.txt.all.3.parsed'
    # indir = '/Users/panx/Desktop/test'
    out = open('/Users/panx/Desktop/out', 'w')
    res = wikify(reader.main(open(indir).read()))
    for i in res:
        out.write('%s\n' % i)
