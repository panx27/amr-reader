'''
 generate html output
'''

import amr_visualizer

def path(name, paths):
    result = '<b>%s</b>\n<br>\n' % name
    p = ''
    for i in paths:
        for j in i:
            role = j[0]
            concept = j[1]
            if role == '@root' or role == '@entity':
                p += '<font face="arial">%s</font>' % concept
            else:
                p += ' --> <font face="verdana" color="orange">%s</font> <font face="arial">%s</font>' % (role, concept)
        p += '<br>'
    return result + p + '\n'

def get_html(senid, sen, amr, output):
    graph = '<img src="./graphs/%s.png">' % senid # default graphs path: ./graphs/
    senid = '<h2>%s</h2>\n' % senid
    sen = '<p><b>%s</b></p>\n' % sen
    amr = '<p>%s</p>\n' % amr.replace('\n', '<br>').replace(' ', '&nbsp;')
    # paths = '<p><b>Paths:</b><br>%s</p><p>%s</p>\n' % (path('root to entity:', paths_rte),
    #                                                        path('entity to leaf:', paths_etl))
    paths = ''
    output.write('<body>\n%s%s%s%s%s</body>\n' % (senid, sen, amr, paths, graph))

def main(amr_table, output=open('../output/test.html', 'w')):
    output.write('<meta charset=\'utf-8\'>\n')

    for docid in sorted(amr_table):
        for senid in sorted(amr_table[docid]):
            s = amr_table[docid][senid]
            amr_visualizer.visualizer(s.amr_nodes_, s.paths_[0], output_name=s.senid_)

            get_html(s.senid_, s.sen_, s.amr_, output)
