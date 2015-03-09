'''
 generate html output
'''

# def html(senid, sen, amr, output):
#     graph = '<img src="./graphs/%s.png">' % senid
#     senid = '<h2>%s</h2>\n' % senid
#     sen = '<p><b>%s</b></p>\n' % sen
#     amr = '<p>%s</p>\n' % amr.replace('\n', '<br>').replace(' ', '&nbsp;')
#     output.write('<body>\n%s%s%s%s</body>\n' % (senid, sen, amr, graph))

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
                p += ' --> <font face="verdana" color="red">%s</font> <font face="arial">%s</font>' % (role, concept)
        p += '<br>'
    return result + p + '\n'

def html(senid, sen, amr, paths_rte, paths_etl, output):
    graph = '<img src="./graphs/%s.png">' % senid
    senid = '<h2>%s</h2>\n' % senid
    sen = '<p><b>%s</b></p>\n' % sen
    amr = '<p>%s</p>\n' % amr.replace('\n', '<br>').replace(' ', '&nbsp;')
    paths = '<p><b>Paths:</b><br>%s</p><p>%s</p>\n' % (path('root to entity:', paths_rte),
                                                           path('entity to leaf:', paths_etl))
    output.write('<body>\n%s%s%s%s%s</body>\n' % (senid, sen, amr, paths, graph))
