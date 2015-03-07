'''
 generate html output
'''

def html(senid, sen, amr, output):
    graph = '<img src="./graphs/%s.png">' % senid
    senid = '<h2>%s</h2>\n' % senid
    sen = '<p><b>%s</b></p>\n' % sen
    amr = '<p>%s</p>\n' % amr.replace('\n', '<br>').replace(' ', '&nbsp;')
    output.write('<body>\n%s%s%s%s</body>\n' % (senid, sen, amr, graph))
